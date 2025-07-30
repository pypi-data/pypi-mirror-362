from abc import ABC
from abc import abstractmethod

from pyakri_de_utils import Constants


class Preprocessor(ABC):
    DST_FILE_FORMAT = "png"
    FEATURIZER_CSV = "featurizer.csv"

    def __init__(self, batch_size: int = 1):
        self.init(batch_size=batch_size)

    def init(self, **kwargs):
        self._batch_size = int(
            kwargs.get("batch_size", Constants.PRE_PROCESSOR_BATCH_SIZE)
        )

    @abstractmethod
    def run(self, in_np_image_list):
        raise NotImplementedError

    @abstractmethod
    def run_from_input_dir(self, src_dir, dst_dir):
        raise NotImplementedError
