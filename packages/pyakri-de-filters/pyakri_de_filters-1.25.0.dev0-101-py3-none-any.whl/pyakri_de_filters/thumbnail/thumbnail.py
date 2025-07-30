from pyakri_de_utils import Constants
from pyakri_de_utils.enums import ResampleAlgoEnum
from pyakri_de_utils.enums import FileTypeEnum
from pyakri_de_utils.file_utils import create_directory
from pyakri_de_utils.file_utils import create_parent_directory
from pyakri_de_utils.file_utils import get_dest_file_path
from pyakri_de_utils.file_utils import get_input_files_dir
from pyakri_de_utils.image_utils import ImageUtils


DEFAULT_RESIZED_WIDTH = -1
DEFAULT_RESIZED_HEIGHT = -1
DEFAULT_RESAMPLE_ALGO = Constants.DEFAULT_THUMBNAIL_RESAMPLE_ALGO
DEFAULT_OUTPUT_FORMAT = Constants.DEFAULT_THUMBNAIL_OUTPUT_FORMAT


class ThumbnailFilter:
    def __init__(
        self,
        width: int = DEFAULT_RESIZED_WIDTH,
        height: int = DEFAULT_RESIZED_HEIGHT,
        resample_algo: ResampleAlgoEnum = DEFAULT_RESAMPLE_ALGO,
        output_format: FileTypeEnum = DEFAULT_OUTPUT_FORMAT,
    ):
        self.init(
            resized_height=height,
            resized_width=width,
            resample_algo=resample_algo,
            output_format=output_format,
        )

    def init(self, **kwargs):
        self._width = int(kwargs.get("resized_width", DEFAULT_RESIZED_WIDTH))
        self._height = int(kwargs.get("resized_height", DEFAULT_RESIZED_HEIGHT))
        self._resample_algo = kwargs.get("resample_algo", DEFAULT_RESAMPLE_ALGO)
        self._output_format = kwargs.get("output_format", DEFAULT_OUTPUT_FORMAT)

    def run(self, src_dir, dst_dir):
        files = get_input_files_dir(directory=src_dir, filter_extensions=set(".csv"))
        if not files:
            raise ValueError("No input files found!")

        create_directory(dst_dir)

        # Generate and save thumbnail
        for file in files:
            img = ImageUtils.get_image_thumbnail(
                file=file,
                resize_dim=(self._width, self._height),
                resample_algo=self._resample_algo,
            )

            dst_path = get_dest_file_path(
                file_path=file, src_dir=src_dir, dst_dir=dst_dir
            )

            create_parent_directory(dst_path)

            ImageUtils.save(
                dst_path,
                img,
                output_format=self._output_format,
            )
