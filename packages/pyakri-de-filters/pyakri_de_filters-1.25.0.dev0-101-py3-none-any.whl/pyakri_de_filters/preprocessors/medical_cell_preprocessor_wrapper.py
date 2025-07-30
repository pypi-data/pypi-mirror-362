import os
from typing import List

from numpy import ndarray
from pyakri_de_filters.preprocessors.main import get_preprocessor_using_args
from pyakri_de_filters.preprocessors.preprocessor import Preprocessor
from pyakri_de_utils.file_utils import copy_file
from pyakri_de_utils.file_utils import create_directory
from pyakri_de_utils.file_utils import get_dest_file_path
from pyakri_de_utils.file_utils import get_input_files_batch
from pyakri_de_utils.image_utils import FileTypeEnum
from pyakri_de_utils.image_utils import ImageUtils


class MedicalCellPreprocessor(Preprocessor):
    PRE_PROCESSOR_ARGS = """--add=correct_gamma --kwargs={} --add=map_color --kwargs={"cmap":"Spectral_r"}"""

    def __init__(self):
        super().__init__()

        self._preprocessor = self._get_preprocessor()

    @classmethod
    def _get_preprocessor(cls):
        preprocessor_args = cls.PRE_PROCESSOR_ARGS.split(" ")
        preprocessor, _, _, _ = get_preprocessor_using_args(preprocessor_args)
        return preprocessor

    def run(self, in_np_image_list: List[ndarray]) -> List[ndarray]:
        return [
            self._preprocessor.fit_transform(np_image) for np_image in in_np_image_list
        ]

    def run_from_input_dir(self, src_dir, dst_dir):
        # Create directories
        create_directory(dst_dir)

        files_generator = get_input_files_batch(src_dir, batch_size=self._batch_size)

        for files in files_generator:
            featurizer_csv_list = []
            np_images_list = []

            for file in files:
                # If filename is featurizer.csv then external featurizer is attached
                # in that case input for featurizer is csv not files
                if file.name == self.FEATURIZER_CSV:
                    featurizer_csv_list.append(file)
                    continue

                img = ImageUtils.get_image_from_file(file)
                img = ImageUtils.convert_image_to_grayscale(img)

                np_images_list.append(img)

            processed_images: List[ndarray] = self.run(np_images_list)

            for i in range(len(processed_images)):
                src_file_path = files[i]
                dest_file_path = get_dest_file_path(
                    file_path=src_file_path, src_dir=src_dir, dst_dir=dst_dir
                )

                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                ImageUtils.save(
                    dest_file_path, processed_images[i], output_format=FileTypeEnum.JPEG
                )

            for file in featurizer_csv_list:
                src_file_path = file
                dest_file_path = get_dest_file_path(
                    file_path=file, src_dir=src_dir, dst_dir=dst_dir
                )

                copy_file(src_file_path, dest_file_path)
