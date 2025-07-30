import os
import tempfile

from data_ingest_filters.data_ingest_filter_wrapper import (
    DataIngestWrapper,
)
from pyakri_de_filters import logger

params_list = [
    "num_components",
    "fraction_rows",
    "fraction_coreset",
    "overwrite",
    "coreset_mode",
    "feature_n",
    "feature_m",
    "feature_f",
    "feature_r",
    "text_search",
    "mem_fraction",
]


def get_init_params(extra_params=None):
    if extra_params is None:
        extra_params = dict()
    init_params = dict()
    for param in params_list:
        param_val = os.environ.get(param, extra_params.get(param))
        if param_val:
            init_params[param] = param_val
    if init_params.get("mem_fraction"):
        os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"] = "false"
        os.environ["XLA_PYTHON_CLIENT_MEM_FRACTION"] = init_params.get("mem_fraction")
    logger.debug(f"Using init params {init_params}")
    return init_params


def run_data_ingest_filter(input_dir, output_dir, extra_params=None):
    if extra_params is None:
        extra_params = dict()
    with tempfile.NamedTemporaryFile() as fp:
        data_ingest_wrapper = DataIngestWrapper()
        data_ingest_wrapper.init(**get_init_params(extra_params))

        data_ingest_wrapper.run(src_dir=input_dir, dst_dir=output_dir, tmp_file=fp.name)

        data_ingest_wrapper.cleanup()
