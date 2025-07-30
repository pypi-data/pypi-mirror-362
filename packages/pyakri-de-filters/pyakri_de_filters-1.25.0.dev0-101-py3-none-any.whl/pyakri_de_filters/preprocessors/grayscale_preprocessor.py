from functools import partial

import matplotlib.pyplot as plt
import numpy as np
from skimage.exposure import adjust_gamma
from skimage.exposure import adjust_log
from skimage.exposure import adjust_sigmoid
from skimage.exposure import equalize_adapthist
from skimage.exposure import equalize_hist
from skimage.filters import apply_hysteresis_threshold
from skimage.filters import threshold_local
from skimage.filters import threshold_otsu


class GrayscalePreprocessors(object):
    def __init__(self):
        self.preprocessing_pipeline = list()

    def add(self, preprocessor, **kwargs):
        """
        Enables preprocessor chaining by adding preprocessors to a pipeline.

        Parameters
        ----------
        preprocessor : str
        **kwargs
            Keyword arguments that will be passed through the preprocessing function.
        """
        func = getattr(self, preprocessor)
        self.preprocessing_pipeline.append(partial(func, **kwargs))

    # Collection of thresholding based pre-processors.
    @staticmethod
    def threshold_global(image, **kwargs):
        """
        References
        ----------
        https://scikit-image.org/docs/dev/api/skimage.filters.html#skimage.filters.threshold_otsu

        Parameters
        ----------
        image : np.array
        **kwargs
            Arguments passed through `skimage.filters.threshold_otsu`

        Returns
        -------
        np.array
        """
        global_thresh = threshold_otsu(image, **kwargs)
        threshed = image >= global_thresh
        threshed = image * threshed
        return threshed

    @staticmethod
    def threshold_local(image, **kwargs):
        """
        References
        ----------
        https://scikit-image.org/docs/stable/api/skimage.filters.html#threshold-local

        Parameters
        ----------
        image : np.array
        **kwargs
            Arguments passed through `skimage.filters.threshold_local`

        Returns
        -------
        np.array
        """
        local_thresh = threshold_local(image, **kwargs)
        threshed = image >= local_thresh
        threshed = image * threshed
        return threshed

    @staticmethod
    def threshold_hysteresis(image, **kwargs):
        """
        References
        ----------
        https://scikit-image.org/docs/stable/api/skimage.filters.html#skimage.filters.apply_hysteresis_threshold

        Parameters
        ----------
        image : np.array
        low : float
        high : float

        Returns
        -------
        np.array
        """
        if kwargs:
            threshed = apply_hysteresis_threshold(image, **kwargs)
        else:
            low = image.mean()
            high = low + image.std()
            threshed = apply_hysteresis_threshold(image, low, high)

        threshed = image * threshed
        return threshed.astype("uint8")

    # Collection of correction based pre-processors.
    @staticmethod
    def correct_gamma(image, **kwargs):
        """
        References
        ----------
        https://scikit-image.org/docs/stable/api/skimage.exposure.html#skimage.exposure.adjust_gamma

        Parameters
        ----------
        image : np.array
        **kwargs
            Arguments passed through `skimage.exposure.adjust_gamma`

        Returns
        -------
        np.array
        """
        return adjust_gamma(image, **kwargs)

    @staticmethod
    def correct_log(image, **kwargs):
        """
        References
        ----------
        https://scikit-image.org/docs/stable/api/skimage.exposure.html#skimage.exposure.adjust_log

        Parameters
        ----------
        image : np.array
        **kwargs
            Arguments passed through `skimage.exposure.adjust_log`

        Returns
        -------
        np.array
        """
        return adjust_log(image, **kwargs)

    @staticmethod
    def correct_sigmoid(image, **kwargs):
        """
        References
        ----------
        https://scikit-image.org/docs/stable/api/skimage.exposure.html#skimage.exposure.adjust_sigmoid

        Parameters
        ----------
        image : np.array
        **kwargs
            Arguments passed through `skimage.exposure.adjust_sigmoid`

        Returns
        -------
        np.array
        """
        return adjust_sigmoid(image, **kwargs)

    # Collection of histogram equalization based pre-processors.
    @staticmethod
    def equalize_histogram(image, **kwargs):
        """
        References
        ----------
        https://scikit-image.org/docs/stable/api/skimage.exposure.html?highlight=exposure#skimage.exposure.equalize_hist

        Parameters
        ----------
        image : np.array
        **kwargs
            Arguments passed through `skimage.exposure.equalize_hist`

        Returns
        -------
        np.array
        """
        equalized_image = equalize_hist(image, **kwargs)
        equalized_image = equalized_image * 255.0
        return equalized_image.astype(np.uint8)

    @staticmethod
    def equalize_adaptive_histogram(image, clip_limit=1, **kwargs):
        """
        References
        ----------
        https://scikit-image.org/docs/stable/api/skimage.exposure.html#skimage.exposure.equalize_adapthist

        Parameters
        ----------
        image : np.array
        **kwargs
            Arguments passed through `skimage.exposure.equalize_adapthist`

        Returns
        -------
        np.array
        """
        equalized_image = equalize_adapthist(image, clip_limit=clip_limit, **kwargs)
        equalized_image = equalized_image * 255.0
        return equalized_image.astype(np.uint8)

    # Color mapping
    @staticmethod
    def map_color(image, cmap="viridis"):
        """
        Parameters
        ----------
        image : np.array
        cmap : str

        Returns
        -------
        np.array
        """
        cm = plt.get_cmap(cmap)
        colored_image = cm(image) * 255.0
        colored_image = colored_image.astype("uint8")

        # Obtain a 4-channel image (R,G,B,A) and clip it to RGB
        return colored_image[:, :, :3]

    def fit_transform(self, image):
        """
        Parameters
        ----------
        image : np.array

        Returns
        -------
        np.array
        """
        for preprocessor in self.preprocessing_pipeline:
            image = preprocessor(image)
        return image
