from abc import ABC
from abc import abstractmethod

import numpy as np
from pyakri_de_filters import logger
from pyakri_de_utils import Constants
from pyakri_de_utils.file_utils import get_input_files_batch
from pyakri_de_utils.image_utils import ImageUtils
from pyakri_de_utils.numpy_utils import save_as_npy_file


class Featurizer(ABC):
    def __init__(self):
        self._batch_size = None
        self._resize_dim = None

    def init(self, **kwargs):
        logger.debug(f"Received init params {kwargs}")

        self._batch_size = int(
            kwargs.get("batch_size", Constants.FEATURIZER_PROCESS_BATCH_SIZE)
        )
        self._resize_dim = kwargs.get(
            "resize_dim", Constants.FEATURIZER_DEFAULT_RESIZED_DIM
        )

    @abstractmethod
    def run(self, in_image_np_list) -> np.ndarray:
        """
        Generate features for this input batch size

        @param in_image_np_list: Input numpy array in batch
        @return numpy array having features for each image stacked
        """
        raise NotImplementedError

    @abstractmethod
    def cleanup(self):
        raise NotImplementedError

    def run_from_input_dir(self, src_dir, dst_dir):
        files_generator = get_input_files_batch(src_dir, batch_size=self._batch_size)

        for files in files_generator:
            features = []

            in_image_np_list = self._read_images(files=files)

            np_arr_list = [np.asarray(in_image_np_list)]

            features_list = self.run(np_arr_list)
            if features_list is None or len(features_list) == 0:
                raise ValueError("No features found after running featurizer!")

            for feature in features_list:
                features.extend(feature)

            save_as_npy_file(
                np_data=np.asarray(features),
                files=files,
                src_dir=src_dir,
                dest_dir=dst_dir,
            )

    def _read_images(self, files):
        img_list = []
        for file in files:
            img = ImageUtils.get_image_from_file(file)
            img = ImageUtils.convert_image_to_rgb(img)
            np_image = ImageUtils.resize(img=img, resize_dim=self._resize_dim)
            img_list.append(np_image)

        return img_list
