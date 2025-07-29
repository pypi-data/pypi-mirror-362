"""
Module for a specialty set of metrics that have a boolean outcome, such as whether a phantom
is in the image or not.
"""
from __future__ import annotations

from typing import Literal

import numpy as np
from scipy import ndimage
from skimage import filters, measure, segmentation

from .image import MetricBase


class SizedBlob(MetricBase):
    """Detect if there is a blob with a certain size in the image."""

    def __init__(self, size: float, units: Literal['mm', 'pixels'], tolerance: float, name="Sized Blob",
                 clip: bool = True, clear_borders: bool = True):
        """

        Parameters
        ----------
        size
        units
        tolerance
        name
        clip
        clear_borders
        """
        self.size = size
        self.units = units
        self.tolerance = (1 + tolerance)
        self.clip = clip
        self.name = name
        self.clear_borders = clear_borders
        super().__init__()

    def calculate(self) -> bool:
        """Get the Scikit-Image ROI of the phantom

        The image is analyzed to see if:
        1) the CatPhan is even in the image (if there were any ROIs detected)
        2) an ROI is within the size criteria of the catphan
        3) the ROI area that is filled compared to the bounding box area is close to that of a circle
        """
        # convert the slice to binary and label ROIs
        edges = filters.scharr(self.image.as_type(float))
        if np.max(edges) < 0.1:
            return False
        # we clip the image to avoid issues where
        # very high or very low HU values cause
        # thresholding problems. E.g. a very high HU bb
        # can make the region detection not see the phantom
        # I can see this causing problems in the future if the
        # HU values are insanely off. This also causes issues
        # with MRI images, which aren't HU values, hence the flag.
        if self.clip:
            clipped_arr = np.clip(self.image.array, a_min=-1000, a_max=1000)
        else:
            clipped_arr = self
        larr, regionprops, num_roi = get_regions(
            clipped_arr,
            fill_holes=True,
            threshold="otsu",
            clear_borders=self.clear_borders,
        )
        # check that there is at least 1 ROI
        if num_roi < 1 or num_roi is None:
            return False
        most_similar_roi = sorted(
            regionprops, key=lambda x: np.abs(x.filled_area - self.size)
        )[0]
        is_too_large = self.size * self.tolerance < most_similar_roi.filled_area
        is_too_small = most_similar_roi.filled_area < self.size / self.tolerance
        if is_too_large or is_too_small:
            return False
        return most_similar_roi


def get_regions(
    array: np.ndarray,
    fill_holes: bool = False,
    clear_borders: bool = True,
    threshold: str = "otsu",
) -> tuple[np.ndarray, list, int]:
    """Get the skimage regions of a black & white image."""
    if threshold == "otsu":
        thresmeth = filters.threshold_otsu
    elif threshold == "mean":
        thresmeth = np.mean
    edges = filters.scharr(array.astype(float))
    edges = filters.gaussian(edges, sigma=1)
    thres = thresmeth(edges)
    bw = edges > thres
    if clear_borders:
        bw = segmentation.clear_border(bw, buffer_size=min(int(max(bw.shape) / 100), 3))
    if fill_holes:
        bw = ndimage.binary_fill_holes(bw)
    labeled_arr, num_roi = measure.label(bw, return_num=True)
    regionprops = measure.regionprops(labeled_arr, edges)
    return labeled_arr, regionprops, num_roi
