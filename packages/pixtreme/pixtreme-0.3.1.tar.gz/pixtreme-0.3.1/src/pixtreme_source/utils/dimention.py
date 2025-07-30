from typing import Literal

import cupy as cp

from ..color.bgr import bgr_to_rgb, rgb_to_bgr
from ..transform.resize import INTER_AUTO, resize
from ..utils.dtypes import to_float32

Layout = Literal["HW", "HWC", "CHW", "NHWC", "NCHW", "ambiguous", "unsupported"]


def guess_image_layout(image: cp.ndarray) -> Layout:
    """
    Infer the layout of an image array.

    Args:
        image (cp.ndarray): The input image array.
    Returns:
        Layout: The inferred layout of the image array.
    """
    nd = image.ndim
    # 2D: HW
    if nd == 2:
        return "HW"
    # 3D: HWC vs CHW
    elif nd == 3:
        c_first, c_last = image.shape[0], image.shape[-1]
        candidates = []
        if c_first in (1, 3, 4):
            candidates.append("CHW")
        if c_last in (1, 3, 4):
            candidates.append("HWC")
        # If candidates is one, return it
        if len(candidates) == 1:
            return candidates[0]
        # Tie-break: channel first vs channel last
        if c_first <= 4 and image.shape[1] > 4 and image.shape[2] > 4:
            return "CHW"
        if c_last <= 4 and image.shape[0] > 4 and image.shape[1] > 4:
            return "HWC"
        return "ambiguous"
    # 4D: NHWC vs NCHW
    elif nd == 4:
        # Candidate 1:  NCHW → (N, C, H, W)
        if image.shape[1] in (1, 3, 4) and image.shape[2] > 4 and image.shape[3] > 4:
            return "NCHW"
        # Candidate 2: NHWC → (N, H, W, C)
        if image.shape[-1] in (1, 3, 4) and image.shape[1] > 4 and image.shape[2] > 4:
            return "NHWC"
        return "ambiguous"
    else:
        return "unsupported"


def batch_to_images(
    batch: cp.ndarray,
    scalefactor: float | None = None,
    mean: float | tuple[float, float, float] | None = None,
    swap_rb: bool = True,
    layout: Layout = "NCHW",
) -> list[cp.ndarray]:
    """
    Convert a batch of images to a list of images.

    Args:
        batch (cp.ndarray): The input batch of images with shape (N, C, H, W) or (N, H, W, C).

    Returns:
        list[cp.ndarray]: A list of images, each with shape (H, W, C).
    """
    if layout != "NCHW":
        layout = guess_image_layout(batch)
        if layout == "NCHW":
            # Convert NCHW to HWC
            batch = batch.transpose(0, 2, 3, 1)
        elif layout == "NHWC":
            pass
        else:
            raise ValueError(f"Unsupported image layout: {layout}")

    results = []
    for image in batch:
        image = image.transpose(1, 2, 0)  # Convert CHW back to HWC
        if swap_rb:
            image = rgb_to_bgr(image)  # Swap RGB to BGR if needed
        if scalefactor is not None:
            image *= 1 / scalefactor
        if mean is not None:
            if isinstance(mean, (int, float)):
                mean = (float(mean), float(mean), float(mean))
            if len(mean) == 1:
                mean = (mean[0], mean[0], mean[0])
            elif len(mean) != 3:
                raise ValueError("Mean must be a single value or a tuple of three values.")
            image += cp.array(mean, dtype=image.dtype)
        results.append(image)

    return results


def images_to_batch(
    images: cp.ndarray | list[cp.ndarray],
    scalefactor: float | None = None,
    size: int | tuple[int, int] | None = None,
    mean: float | tuple[float, float, float] | None = None,
    swap_rb: bool = True,
    layout: Layout = "HWC",
) -> cp.ndarray:
    """
    Convert a list of images to batches.
    """
    if isinstance(images, list):
        # Convert a list of images to a batch
        results = []
        for image in images:
            result = image_to_batch(
                image,
                scalefactor=scalefactor,
                size=size,
                mean=mean,
                swap_rb=swap_rb,
                layout=layout,
            )
            results.append(result)
        return cp.concatenate(results, axis=0)

    image: cp.ndarray = images
    return image_to_batch(
        image,
        scalefactor=scalefactor,
        size=size,
        mean=mean,
        swap_rb=swap_rb,
        layout=layout,
    )


def image_to_batch(
    image: cp.ndarray,
    scalefactor: float | None = None,
    size: int | tuple[int, int] | None = None,
    mean: float | tuple[float, float, float] | None = None,
    swap_rb: bool = True,
    layout: Layout = "HWC",
) -> cp.ndarray:
    """
    Convert a single image to a batch.
    """

    if layout not in ["HWC", "HW", "CHW", "NHWC", "NCHW"]:
        layout = guess_image_layout(image)

    if layout == "NCHW":
        return image
    elif layout == "NHWC":
        # Convert NHWC to NCHW
        return image.transpose(0, 3, 1, 2)
    elif layout == "HW":
        image = image[..., cp.newaxis]
        layout = "HWC"

    array_dtype = image.dtype

    # swap RB
    if swap_rb and layout in ["HWC", "NHWC"]:
        image = bgr_to_rgb(image)

    # size
    if size is not None:
        if isinstance(size, int):
            size = (size, size)
        image = resize(image, dsize=size, interpolation=INTER_AUTO)

    # mean
    if mean is not None:
        if isinstance(mean, (int, float)):
            mean = (float(mean), float(mean), float(mean))
        if len(mean) == 1:
            mean = (mean[0], mean[0], mean[0])
        elif len(mean) != 3:
            raise ValueError("Mean must be a single value or a tuple of three values.")
        image -= cp.array(mean, dtype=array_dtype)

    # scalefactor
    if scalefactor is not None:
        image *= scalefactor

    # layout conversion
    if layout == "HWC":
        # Convert HWC to NCHW
        return image.transpose(2, 0, 1)[cp.newaxis, ...]
    elif layout == "CHW":
        # Convert CHW to NCHW
        return image[cp.newaxis, ...]
    else:
        raise ValueError(f"Unsupported image layout: {layout}")
