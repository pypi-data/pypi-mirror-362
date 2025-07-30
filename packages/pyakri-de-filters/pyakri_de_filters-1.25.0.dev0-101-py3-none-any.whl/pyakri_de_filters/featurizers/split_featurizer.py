import numpy as np
from pyakri_de_filters import logger
from pyakri_de_utils.enums import ResampleAlgoEnum
from pyakri_de_utils.image_utils import ImageUtils

from .image_featurizer import ImageFeaturizer


class SplitFeaturizer(ImageFeaturizer):
    def __init__(self):
        super().__init__()
        self._feature_m = None
        self._feature_n = None

    def init(self, **kwargs):
        super().init(**kwargs)

        self._feature_m = int(kwargs.get("feature_m", "5"))
        self._feature_n = int(kwargs.get("feature_n", "5"))
        logger.debug(
            f"Using mxn for Split featurizer as {self._feature_m}x{self._feature_n}"
        )

    @staticmethod
    def patchify(image, grid_shape):
        """
        The patchify function takes an image and a grid shape (in the form of a tuple) as input.
        It then divides the image into tiles of equal size, given by grid_shape.
        The function returns a numpy array containing all these tiles in a grid.

        Parameters
        ----------
        image: ndarray of shape (imrows, imcols, n_channels)
            Image to be converted into tiles.

        grid_shape: 2-tuple of int
            Grid to use for tiling, as (grows, gcols)

        Returns
        -------
        tiled_image: ndarray of shape (grows, gcols, imrows//grows, imcols//gcols, ...)
            Tiled image.

        Examples
        --------
        Let's tile a simple numpy array.
        >>> img = np.arange(24, dtype=int).reshape(4, 6)
        >>> tiled_img = patchify(img, (2, 2))
        >>> tiled_img[0, 0]
        array([[0, 1, 2],
               [6, 7, 8]])
        >>> tiled_img[0, 1]
        array([[ 3,  4,  5],
               [ 9, 10, 11]])
        """
        image_shape = image.shape

        if (image_shape[0] % grid_shape[0] != 0) or (
            image_shape[1] % grid_shape[1] != 0
        ):
            raise ValueError(
                "Image rows and columns should be integer multiples of grid rows and cols."
            )

        # For grayscale images, add an extra axis at the end to have consistent logic later.
        if len(image.shape) == 2:
            image = image[:, :, np.newaxis]
            added_axis = True
        else:
            added_axis = False

        imrows, imcols = image_shape[0], image_shape[1]
        grows, gcols = grid_shape[0], grid_shape[1]

        # We'll use numpy reshapes to do this.
        # 1. Tile along columns and rows.
        tiled_image = image.reshape(
            (grows, imrows // grows, gcols, imcols // gcols, -1)
        )
        # 2. Swap axis for rows grid rows and cols.
        tiled_image = np.swapaxes(tiled_image, 1, 2)

        # If we added an axis previously for grayscale images, get rid of it.
        if added_axis:
            tiled_image = tiled_image.squeeze(axis=-1)

        return tiled_image

    def run(self, in_image_np_list):
        features_np_list = []
        for image_batch in in_image_np_list:
            upsampled_batch = []
            for image in image_batch:
                upsample_image = ImageUtils.resize(
                    image,
                    (224 * self._feature_m, 224 * self._feature_n),
                    ResampleAlgoEnum.LINEAR,
                )
                upsampled_batch.append(
                    self.patchify(upsample_image, (self._feature_m, self._feature_n))
                )

            upsampled_batch = np.stack(upsampled_batch)
            upsampled_batch = upsampled_batch.reshape((-1, 224, 224, 3))
            image_batch = self.preprocessor(upsampled_batch)
            image_batch = image_batch.astype(self.input_type)
            output = self.session.run(
                [self.output_name], {self.input_name: image_batch}
            )
            features_np_list.append(
                output[0].reshape(
                    (-1, self._feature_m, self._feature_n, output[0].shape[-1])
                )
            )

        features_np_list = np.stack(features_np_list)
        return features_np_list
