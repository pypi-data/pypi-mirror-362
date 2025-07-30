""" Script to process featurizer output to generate low dimensional input """
import math
from functools import reduce
from time import perf_counter

import numpy as np
from akriml.sketch.fastsketch import FastSketch
from pandas import DataFrame

from . import logger
from .utils import get_LWCS_util_methods

LWCS_dual, LWCS_kmeans = get_LWCS_util_methods()


class DataIngestFilter:
    """
    Python script to apply matrix sketch and coreset algorithms to the output
    of mobilenet featurizer to reduce the dimensions of features
     for further analysis

    Examples
    --------
    This is a simple test to verify the shapes of outputs. Let's create two numpy arrays,
    one for image-level features, and another for patch-level features.

    >>> n_samples = 500  # Total frames
    >>> n_features = 64  # Original feature space dimensionality
    >>> n_patch_rows = 3  # For patch features; we'll use n_rows = n_cols
    >>> image_features = np.random.rand(n_samples, n_features)
    >>> patch_features = np.random.rand(n_samples, n_patch_rows, n_patch_rows, n_features)

    For filter params, we'll ask for reduction to 8d and coreset sampling of 10%. Note that
    true coreset sampling is only available via adectl (statsum). In AkriSDK, this is
    replaced by uniform sampling.

    >>> n_components = 8  # Reduced dimensionality
    >>> fraction_coreset = 0.1

    Initialize filter

    >>> filter = DataIngestFilter()
    >>> filter.init(num_components=n_components, feature_n=n_patch_rows,
    ...             feature_m=n_patch_rows, feature_f=n_features,
    ...             fraction_coreset=fraction_coreset)

    Run on input data; first on image-features. For some reason, the output is not a list of
    values, but a list of lists. So each output has to be indexed again;

    >>> proj_df, coreset_df, sketch = filter.run_common(image_features)
    >>> np.array(proj_df[0]['projections'].tolist()).shape  # (n_samples, n_components)
    (500, 8)
    >>> np.array(coreset_df[0]['values'].tolist()).shape  # (fraction_coreset*n_sample, ...)
    (50, 8)
    >>> sketch[0].shape  # (n_components, n_features)
    (8, 64)

    And on patch-features, the output is still a 2d array where the last axis contains patch
    features after they are flattened. So we get 3*3*8=72 features per image.

    >>> proj_df, coreset_df, sketch = filter.run_common(patch_features)
    >>> np.array(proj_df[0]['projections'].tolist()).shape
    (500, 72)
    >>> np.array(coreset_df[0]['values'].tolist()).shape  # (fraction_coreset*n_sample, ...)
    (50, 72)
    >>> sketch[0].shape  # (n_components, n_features)
    (8, 64)
    """

    _PROJECTION_COLUMNS = ["projections", "representation_error"]
    _CORESET_COLUMNS = ["values", "weights", "indices"]
    _CORESET_MODES = ["dual", "kmeans"]

    def __init__(self):
        """
        The constructor takes no arguments, for consistency with other filters.
        See .init() for details.
        """
        self.num_components = 24
        self.fraction_rows = 0.5
        self.overwrite = True
        self.fast_sketch = None
        self.fraction_coreset = 0.1
        self.coreset_mode = "kmeans"
        self.feature_n = 1
        self.feature_m = 1
        self.feature_f = 1280
        self.feature_r = 0

    def init(self, **kwargs):
        """
        Sets filter parameters.

        Parameters
        ----------
        num_components: int, default=24 (see __init__ body)
            Number of reduced dimensions in output (per patch)
        feature_n: int, default=1
            Number of columns in patch grid
        feature_m: int, default=1
            Number of rows in patch grid
        feature_f: int, default=1280
            Number of features (per-patch) in input (from featurizer)
        fraction_rows: float, default=0.3
            Fraction of rows to use for initial dimensionality reduction.
            Setting this to 1 makes the reduction more accurate.
            Lower values make it faster, but less accurate.
        fraction_coreset: float, default=0.3
            Size of coreset, as a fraction of input.
        coreset_mode: str, default='kmeans'
            Method to create coreset.
            Acceptable values are 'kmeans', 'ksegment', 'dual'.
        overwrite: bool, default=True
            If True, subsequent runs of the same initialized filter will reset
                the underlying dimensionality reduction (MatrixSketch).
            If False, subsequent runs incrementally train the reduction.
        """
        self.num_components = int(kwargs.get("num_components", self.num_components))
        self.feature_n = int(kwargs.get("feature_n", self.feature_n))
        self.feature_m = int(kwargs.get("feature_m", self.feature_m))
        self.feature_f = int(kwargs.get("feature_f", self.feature_f))
        self.feature_r = int(kwargs.get("feature_r", self.feature_r))
        self.skip_rotate = str(kwargs.get("text_search")).upper() == "TRUE"
        # num_components has to be set to be equal to the feature_f to skip dimensionality reduction
        if self.skip_rotate:
            self.num_components = self.feature_f
        self.fraction_rows = float(kwargs.get("fraction_rows", self.fraction_rows))
        if not 0 < self.fraction_rows <= 1:
            raise ValueError("Invalid fraction_rows. Should be in range (0, 1]")
        self.fraction_coreset = float(
            kwargs.get("fraction_coreset", self.fraction_coreset)
        )
        if not 0 < self.fraction_coreset <= 1:
            raise ValueError("Invalid fraction_coreset. Should be in range (0, 1]")
        self.overwrite = bool(kwargs.get("overwrite", self.overwrite))
        self.coreset_mode = self._parse_coreset_mode(
            kwargs.get("coreset_mode", self.coreset_mode)
        )
        self.fast_sketch = None

    def run_common(self, in_np_merged):
        """
        Run dimensionality reduction and return dataframes.

        Parameters
        ----------
        in_np_merged: numpy array of shape (n_samples, ..., n_features)
            Input features.
            For 1d features, shape is (n_samples, n_features).
            For 3d features, shape is (n_samples, n_rows, n_cols, n_features).

        Returns
        -------
        A list containing the following lists:
        projections_df: DataFrame
            Contains columns 'projections' and 'rep_error'
        coreset_df: DataFrame
            Contains columns 'values', 'weights', 'indices' for the
                projections, weights, and indices for coreset samples.
        sketch: numpy array of shape (num_components, features_f)
            Sketch for the patchwise dimensionality reduction.
        The 'projections' and 'values' columns in the dataframes contain
            projections of shape (n_samples, num_components) or
                (n_samples, feature_m*feature_n*num_components) for the
                1d and 3d feature case respectively.
        """
        ec_time = 0  # time taken for error calculation
        pr_time = 0  # time taken for generating projections
        cs_time = 0  # time taken for coreset generation

        if self.feature_r:
            # for region featurizer reshape 2d array input for each image to 1d
            prev_in_np_shape = in_np_merged.shape
            in_np_merged = in_np_merged.reshape(-1, self.feature_f)
            logger.info(
                f"Input numpy array reshaped from {prev_in_np_shape} to {in_np_merged.shape}"
            )

        # 3 lists for 3 output ports
        n_blocks = math.ceil(
            reduce(lambda x, y: x * y, in_np_merged.shape[:-1]) / 200_000
        )
        self.fast_sketch = FastSketch(
            n_components=self.num_components,
            frac=self.fraction_rows,
            overwrite=self.overwrite,
            skip_rotate=self.skip_rotate,
            n_blocks=n_blocks,
        )
        logger.debug(
            f"Shape of input numpy array for fast sketch: {in_np_merged.shape}, n_blocks:{n_blocks}"
        )
        pr_start = perf_counter()

        # matrix sketch algorithm
        projections = self.fast_sketch.fit_transform(in_np_merged)
        pr_time += perf_counter() - pr_start

        ec_start = perf_counter()
        # Representation error measures information loss (during reconstruction).
        # This was intended to inform us of the quality of dimensionality reduction.
        # However, we don't use this information at all.
        # Because calculating this error is expensive, and we don't use it,
        #   we'll skip it altogether.
        # For backwards compatibility, we'll assign dummy values.
        rep_error = np.zeros(len(in_np_merged))
        ec_time += perf_counter() - ec_start

        # generate projections data frame with projections
        # and error columns
        projections_df = self._generate_dataframe(
            self._PROJECTION_COLUMNS, projections, rep_error
        )
        projections_df["projections"] = self._flatten_np_list_elements(
            projections_df["projections"].to_numpy()
        )

        cs_start = perf_counter()
        # Coreset generation from low weighted coreset algorithm
        if self.coreset_mode == "dual":
            cs_points, cs_weights, cs_indices = LWCS_dual(
                projections, frac=self.fraction_coreset
            )
        elif self.coreset_mode == "kmeans":
            cs_points, cs_weights, cs_indices = LWCS_kmeans(
                projections, frac=self.fraction_coreset
            )
        else:
            raise ValueError(f"unsupported coreset_mode: {self.coreset_mode}")
        cs_time += perf_counter() - cs_start

        #  generate coreset pdf with values, weights and indices
        coreset_modified = self._generate_dataframe(
            self._CORESET_COLUMNS, cs_points, cs_weights, cs_indices
        )
        coreset_modified["values"] = self._flatten_np_list_elements(
            coreset_modified["values"].to_numpy()
        )

        proj_arr = np.array(projections_df["projections"].tolist())
        logger.debug(f"Projections df shape: (1, {str(projections_df.shape)[1:]}")
        logger.debug(f"Projections arr shape: {proj_arr.shape}")
        logger.debug(f"Coreset shape: (1, {str(coreset_modified.shape)[1:]}")
        logger.debug(f"Sketch shape: (1, {str(self.fast_sketch.sketch.shape)[1:]}")

        logger.debug(
            f"Time taken for error calculation: {ec_time}, "
            f"Projections: {pr_time}, Coreset: {cs_time}"
        )

        # TODO: Change the ouptut format; list of lists seems unintuitive
        return [[projections_df], [coreset_modified], [self.fast_sketch.sketch]]

    @staticmethod
    def _generate_dataframe(columns, *args):
        return DataFrame(zip(*args), columns=columns)

    @staticmethod
    def _flatten_np_list_elements(np_list):
        if np_list[0].ndim <= 1:
            return np_list
        array_2d = []
        for element in np_list:
            array_2d.append(element.ravel())
        return array_2d

    def _parse_coreset_mode(self, mode):
        """
        :param mode: string value for coreset_mode [dual, kmeans]
        :return: chosen mode after parsing
        """
        mode = mode.lower()
        if mode in self._CORESET_MODES:
            return mode
        else:
            raise ValueError(f"unsupported coreset_mode: {mode}")

    def cleanup(self):
        pass
