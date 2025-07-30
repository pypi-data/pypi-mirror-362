import argparse
import json
import sys
from collections import namedtuple
from glob import glob
from pathlib import Path

import numpy as np
from pyakri_de_filters.preprocessors.grayscale_preprocessor import (
    GrayscalePreprocessors,
)
from pyakri_de_filters.preprocessors.none_preprocessor import NonePreprocessor
from pyakri_de_utils.image_utils import FileTypeEnum
from pyakri_de_utils.image_utils import ImageUtils
from tqdm import tqdm

Preprocessor = namedtuple("Preprocessor", ["name", "kwargs"])


def init_preprocessing_pipeline(preprocessor_chain_list):
    """
    Parameters
    ----------
    preprocessor_chain_list : list
        List of Preprocessor namedtuple objects

    Returns
    -------
    GrayscalePreprocessors object
    """
    _preprocessor = GrayscalePreprocessors()
    for pp in preprocessor_chain_list:
        _preprocessor.add(pp.name, **pp.kwargs)
    return _preprocessor


def main():
    """
    get preprocessor on basis of command line arguments and then run it
    on input dir files and store the output in destination directory
    """
    preprocessor, src_dir, dst_dir, verbose = get_preprocessor_using_args(sys.argv[1:])

    is_src_or_dst_param_missing = False
    if src_dir == "" or src_dir is None:
        is_src_or_dst_param_missing = True
        print("--input_dir param is required")

    if dst_dir == "" or dst_dir is None:
        is_src_or_dst_param_missing = True
        print("--output_dir param is required")
    if is_src_or_dst_param_missing:
        sys.exit()

    # if preprocessor is of NonePreprocessor type then don't process the data
    if isinstance(preprocessor, NonePreprocessor):
        sys.exit("No preprocessor argument passed")

    # make dirs if doesn't exist
    for path in [src_dir, dst_dir]:
        Path(path).mkdir(parents=True, exist_ok=True)

    # Iterate over all files in source directory
    for image_path in tqdm(glob(f"{src_dir}/*"), disable=not verbose):
        image = ImageUtils.convert_image_to_grayscale(
            ImageUtils.get_image_from_file(Path(image_path))
        )

        processed_image = preprocessor.fit_transform(np.asarray(image))

        # save as png
        file_name: str = Path(image_path).name

        ImageUtils.save(
            Path(f"{dst_dir}/{file_name}"), processed_image, FileTypeEnum.PNG
        )


def get_preprocessor_using_args(input_args):
    """
    Parameters
    ----------
    input_args : list
        List of input arguments to create a preprocesor

    Returns
    -------
    GrayscalePreprocessors object
    verbose boolean
    """
    # initialize argument parser
    parser = argparse.ArgumentParser()
    # preprocessor name
    parser.add_argument(
        "--add",
        action="append",
        type=str,
        choices=[
            "threshold_global",
            "threshold_local",
            "threshold_hysteresis",
            "correct_gamma",
            "correct_log",
            "correct_sigmoid",
            "equalize_histogram",
            "equalize_adaptive_histogram",
            "map_color",
        ],
    )
    # keyword arguments
    parser.add_argument(
        "--kwargs",
        action="append",
        type=json.loads,
        help="""Example: --kwargs={\"clip_limit\":1.0} or --kwargs={}""",
    )
    # verbosity
    parser.add_argument("--verbose", default=False, type=bool)
    # custom input directory
    parser.add_argument("--input_dir", type=str)
    # custom output directory
    parser.add_argument("--output_dir", type=str)

    # get parsed arguments
    args = parser.parse_args(args=input_args)

    # set i/o directories
    src_dir = args.input_dir
    dst_dir = args.output_dir

    # if no arguments passed
    if args.add is None:
        none_preprocessor = NonePreprocessor()
        return none_preprocessor, src_dir, dst_dir, args.verbose

    if len(args.kwargs) != len(args.add):
        parser.error(
            "Number or arguments --add and --kwargs should be equal. "
            "In case of no kwargs, pass --kwargs={}"
        )

    preprocessor_chain = []
    for arguments in list(zip(args.add, args.kwargs)):
        preprocessor_chain.append(Preprocessor(arguments[0], arguments[1]))

    preprocessor = init_preprocessing_pipeline(preprocessor_chain)
    return preprocessor, src_dir, dst_dir, args.verbose


if __name__ == "__main__":
    main()
