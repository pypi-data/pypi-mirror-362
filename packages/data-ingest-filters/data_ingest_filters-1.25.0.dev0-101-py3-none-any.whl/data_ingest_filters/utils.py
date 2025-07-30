import numpy as np


def _LWCS_dual(X, t=None, n=None, frac=0.1, **kwargs):
    """
    Return a uniform sample from input.
    Output is a tuple of features, weights, and indices.
    This replaces the calls to LWCS coresets provided by statsum.sample

    Examples
    --------
    Sample 4 out of 40 points

    >>> X = np.random.rand(40, 6)  # 40 samples in 6d feature space
    >>> feat, wts, inds = _LWCS_dual(X, frac=0.1)
    >>> wts  # Should be 10, because each sample stands for 10 in input
    array([10., 10., 10., 10.])
    >>> inds
    array([ 0, 10, 20, 30])
    >>> np.array_equal(X[::10], feat)  # Every 10th sample is picked
    True

    Output size cannot go beyond the input

    >>> feat, wts, inds = _LWCS_dual(X,  n=50)  # `n` value gets capped to len(X)
    >>> np.array_equal(feat, X)
    True
    >>> np.array_equal(wts, [1.]*len(X))
    True
    >>> np.array_equal(inds, range(40))
    True

    Sampling on empty data returns empty output

    >>> feat, wts, inds = _LWCS_dual(np.empty((0, 16)), n=5)  # `n` value is irrelevant
    >>> len(feat), len(wts), len(inds)
    (0, 0, 0)
    """
    if len(X) == 0:
        # If the input data is empty, return dummy output.
        return np.zeros(X.shape), np.array([]), np.array([])

    if n is None:
        # Pick at least one sample to return
        n = max(int(frac * len(X)), 1)

    n = min(n, len(X))  # Can't return more samples than in the input.

    sample_indices = np.linspace(0, len(X), num=n, endpoint=False, dtype=int)
    sample_features = X[sample_indices]
    sample_weights = len(X) / n * np.ones(len(sample_features))
    return sample_features, sample_weights, sample_indices


def get_LWCS_util_methods():
    return _LWCS_dual, _LWCS_dual


if __name__ == "__main__":
    import doctest

    print("Running doctests...")
    doctest.testmod()
