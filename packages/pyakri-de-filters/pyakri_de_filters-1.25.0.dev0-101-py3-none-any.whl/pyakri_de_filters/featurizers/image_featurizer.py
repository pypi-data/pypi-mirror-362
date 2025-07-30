import gc
import marshal
import os
import types

import numpy as np
from pyakri_de_filters.featurizers.featurizer import Featurizer
from pyakri_de_utils.onnx_utils import get_onnx_session

dtype_list = {
    "tensor(float)": np.float32,
    "tensor(double)": np.float64,
    "tensor(half)": np.float16,
    "tensor(long)": np.int64,
    "tensor(int)": np.int32,
}


class ImageFeaturizer(Featurizer):
    data_path = os.path.join(os.path.split(__file__)[0], "../data")

    def __init__(self):
        super().__init__()
        self.debug = False
        self.session = None

        self.model_name = None
        self.input_name = None
        self.input_shape = None
        self.input_type = None
        self.output_name = None
        self.output_shape = None
        self.output_type = None
        self.preprocessor = None
        self.gpu_mem_fraction = None

    @classmethod
    def available_models(cls):
        data_dir = os.path.join(cls.data_path, "models")
        model_files = [
            f.split(".onnx")[0] for f in os.listdir(data_dir) if ".onnx" in f
        ]
        return model_files

    def init(self, **kwargs):
        super().init(**kwargs)

        self.model_name = kwargs.get("model")
        onnx_file = os.path.join(self.data_path, "models", self.model_name + ".onnx")
        self.session = get_onnx_session(
            onnx_model=onnx_file,
            providers=kwargs.get("providers"),
            gpu_mem_fraction=kwargs.get("mem_fraction"),
        )

        self.get_io_config()
        self.load_preprocessor()

    def get_io_config(self):
        self.input_name = self.session.get_inputs()[0].name
        self.input_shape = self.session.get_inputs()[0].shape
        self.input_type = dtype_list[self.session.get_inputs()[0].type]

        self.output_name = self.session.get_outputs()[0].name
        self.output_shape = self.session.get_outputs()[0].shape
        self.output_type = dtype_list[self.session.get_outputs()[0].type]

    def load_preprocessor(self):
        # the convention should be that preprocessor gets the input
        # (batch_size, dim, dim, channels)
        preprocessor_file = os.path.join(
            self.data_path, "preprocessors", self.model_name + ".preprocessor"
        )
        with open(preprocessor_file, "rb") as file_handle:
            binary_code = file_handle.read()
        code = marshal.loads(binary_code)
        self.preprocessor = types.FunctionType(code, globals(), "preprocessor")

    def run(self, in_image_np_list):
        features_np_list = []
        for image_batch in in_image_np_list:
            image_batch = self.preprocessor(image_batch)
            image_batch = image_batch.astype(self.input_type)
            output = self.session.run(
                [self.output_name], {self.input_name: image_batch}
            )
            features_np_list.append(output)

        features_np_list = np.vstack(features_np_list)
        return features_np_list

    def cleanup(self):
        del self.session
        gc.collect()

    def __repr__(self):
        if self.model_name is None:
            return "Uninitialized featurizer object"
        else:
            return str(
                {
                    "model_name": self.model_name,
                    "input_shape": self.input_shape,
                    "output_shape": self.output_shape,
                }
            )
