from pyakri_de_filters.preprocessors.default_preprocessor_wrapper import (
    DefaultPreprocessorWrapper,
)
from pyakri_de_filters.preprocessors.enums import PreProcessorType
from pyakri_de_filters.preprocessors.medical_cell_preprocessor_wrapper import (
    MedicalCellPreprocessor,
)
from pyakri_de_utils import Constants


def get_preprocessor(preprocessor_type: PreProcessorType, **kwargs):
    if preprocessor_type == PreProcessorType.DEFAULT:
        preprocessor = DefaultPreprocessorWrapper()
    elif preprocessor_type == PreProcessorType.MEDICAL_CELLS:
        preprocessor = MedicalCellPreprocessor()
    else:
        raise ValueError(f"Preprocessor '{preprocessor_type}' is not supported!")

    preprocessor.init(**kwargs)
    return preprocessor


def run_preprocessor(
    preprocessor_type: PreProcessorType,
    src_dir: str = Constants.DEFAULT_FILTER_INPUT_DIR,
    dst_dir: str = Constants.DEFAULT_FILTER_OUTPUT_DIR,
    **kwargs,
):
    preprocessor = get_preprocessor(preprocessor_type, **kwargs)
    preprocessor.run_from_input_dir(
        src_dir=src_dir,
        dst_dir=dst_dir,
    )
