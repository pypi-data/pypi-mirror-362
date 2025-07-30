import numpy as np
from pyakri_de_filters import logger
from pyakri_de_utils.data_converter_utils import DataConverters
from pyakri_de_utils.data_converter_utils import Field
from pyakri_de_utils.data_converter_utils import Schema
from pyakri_de_utils.file_utils import create_directory
from pyakri_de_utils.file_utils import get_input_files_dir
from pyakri_de_utils.numpy_utils import get_flattened_np_array


class FeaturizerAggregator:
    FEATURE_COL = "features"
    INPUT_FILE_EXTEN = ".npy"
    DEST_ARROW_FILE = "0-1"

    def __init__(self):
        self._data_converter = DataConverters()

    def init(self, *kwargs):
        pass

    def _write_output(self, np_arr_list, dst_dir, file_name):
        create_directory(dst_dir)

        schema = Schema([Field(self.FEATURE_COL, "float32[]")], "numpy")

        np_data = np.asarray(np_arr_list)
        arrow = self._data_converter.numpy_to_arrow(np_data, schema)

        self._data_converter.arrow_to_arrow_file(dst_dir, file_name, arrow)

    def run(self, src_dir, dst_dir):
        files = get_input_files_dir(directory=src_dir, extension=self.INPUT_FILE_EXTEN)
        if not files:
            raise ValueError("No input files found!")

        flatten_np_list = []
        for file in files:
            flatten_np_list.append(get_flattened_np_array(file))

        logger.info(
            f"Dimension is {flatten_np_list[0].ndim} and shape is "
            f"{flatten_np_list[0].shape} after flattening npy file"
        )

        self._write_output(
            np_arr_list=flatten_np_list, dst_dir=dst_dir, file_name=self.DEST_ARROW_FILE
        )
