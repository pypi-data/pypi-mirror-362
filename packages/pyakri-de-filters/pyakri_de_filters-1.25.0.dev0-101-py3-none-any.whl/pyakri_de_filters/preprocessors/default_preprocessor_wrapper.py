from typing import List

from numpy import ndarray
from pyakri_de_filters.preprocessors.preprocessor import Preprocessor
from pyakri_de_utils.file_utils import copy_file
from pyakri_de_utils.file_utils import create_directory
from pyakri_de_utils.file_utils import get_dest_file_path
from pyakri_de_utils.file_utils import get_input_files_batch


class DefaultPreprocessorWrapper(Preprocessor):
    def run(self, in_np_image_list: List[ndarray]):
        return in_np_image_list

    def run_from_input_dir(self, src_dir, dst_dir):
        # Create directories
        create_directory(dst_dir)

        files_generator = get_input_files_batch(src_dir, batch_size=self._batch_size)
        for files in files_generator:
            for file in files:
                dst_path = get_dest_file_path(
                    file_path=file, src_dir=src_dir, dst_dir=dst_dir
                )

                copy_file(file, dst_path)
