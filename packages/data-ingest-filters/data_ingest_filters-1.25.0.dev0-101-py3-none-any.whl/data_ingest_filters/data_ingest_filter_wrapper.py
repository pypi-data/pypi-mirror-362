import os

import pandas as pd
import pyarrow as pa
from pyakri_de_utils.file_utils import create_directories
from pyakri_de_utils.numpy_utils import get_mem_mapped_np_array

from .data_ingest_filter import DataIngestFilter


class DataIngestWrapper(object):
    DEST_PROJECTIONS_SUB_DIR = "o1/"
    DEST_CORESET_SUB_DIR = "o2/"
    DEST_SKETCH_SUB_DIR = "o3/"

    OUT_DIRS = [DEST_PROJECTIONS_SUB_DIR, DEST_CORESET_SUB_DIR, DEST_SKETCH_SUB_DIR]
    FEATURES = "features"

    def __init__(self):
        self._data_ingest = DataIngestFilter()

    def init(self, **kwargs):
        self._data_ingest.init(**kwargs)

    def compute(self, np_list, file_name, dst_dir):
        projections_df, coreset_modified, sketch = self._data_ingest.run_common(np_list)

        projections_df_dir = os.path.join(dst_dir, self.DEST_PROJECTIONS_SUB_DIR)
        coreset_df_dir = os.path.join(dst_dir, self.DEST_CORESET_SUB_DIR)
        sketch_df_dir = os.path.join(dst_dir, self.DEST_SKETCH_SUB_DIR)

        self.write_arrow(projections_df, projections_df_dir, file_name)
        self.write_arrow(coreset_modified, coreset_df_dir, file_name)
        self.write_arrow(sketch, sketch_df_dir, file_name, True)

    def cleanup(self):
        self._data_ingest.cleanup()

    @staticmethod
    def write_arrow(data_list, dest_prefix, file_name, is_numpy=False):
        data = data_list[0]
        if is_numpy:
            if data.ndim == 1:
                arr = pa.array(data)
                table = pa.Table.from_arrays([arr])
            else:
                # Handles multi-dim cases by reducing them to 2D
                # Because Arrow doesn't support Tensors as col-types
                if data.shape[0] != 0:
                    data = data.reshape(data.shape[0], -1)
                obj = pd.DataFrame([[_] for _ in data])
                table = pa.Table.from_pandas(obj)
        else:
            table = pa.Table.from_pandas(data)

        sink = os.path.join(dest_prefix + file_name)
        writer = pa.RecordBatchStreamWriter(sink, table.schema)
        writer.write(table)
        writer.close()

    @classmethod
    def _create_directories(cls, dst_dir):
        paths = [os.path.join(dst_dir, dest_sub_dir) for dest_sub_dir in cls.OUT_DIRS]

        create_directories(paths)

    def run(self, src_dir, dst_dir, tmp_file):
        self._create_directories(dst_dir=dst_dir)

        np_list = get_mem_mapped_np_array(src_dir=src_dir, temp_fp=tmp_file)
        self.compute(np_list, "0-1.arrow", dst_dir)
