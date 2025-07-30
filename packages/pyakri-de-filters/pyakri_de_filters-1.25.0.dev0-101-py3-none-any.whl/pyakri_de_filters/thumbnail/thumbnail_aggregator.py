import os

import pandas as pd
from pyakri_de_filters import logger
from pyakri_de_utils.arrow_utils import write_arrow_from_df
from pyakri_de_utils.file_utils import create_directory
from pyakri_de_utils.file_utils import get_input_files_dir
from pyakri_de_utils.numpy_utils import get_bytes_from_img


class ThumbnailAggregator:
    DF_COLUMNS = ["thumbnail", "filename"]
    DEST_ARROW_FILE = "0-1"

    def __init__(self):
        pass

    def init(self, *kwargs):
        pass

    def _write_output(self, im_arr_list, dst_dir):
        create_directory(dst_dir)

        data_frame_to_write = pd.DataFrame(im_arr_list, columns=self.DF_COLUMNS)
        dst_arrow_file_path = os.path.join(dst_dir, self.DEST_ARROW_FILE)

        write_arrow_from_df(data_frame_to_write, dst_arrow_file_path)

    def run(self, src_dir, dst_dir):
        files = get_input_files_dir(directory=src_dir)
        if not files:
            raise ValueError("No input files found!")

        im_arr_list = []
        for file in files:
            try:
                img_bytes = get_bytes_from_img(file)
                im_arr_list.append([img_bytes, str(file)[len(src_dir) :]])
            except Exception as ex:
                logger.error("Failed to generate bytes for {}".format(file))
                raise ex

        if len(im_arr_list) == 0:
            logger.error("Input file list to create bytes is empty")
            raise ValueError("Input file list to create bytes is empty")

        self._write_output(im_arr_list=im_arr_list, dst_dir=dst_dir)
