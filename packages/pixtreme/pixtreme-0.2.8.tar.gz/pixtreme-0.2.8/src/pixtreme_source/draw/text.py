import cupy as cp
import cv2

from ..transform.resize import INTER_AUTO, resize
from ..utils.dlpack import to_cupy, to_numpy


def put_text(
    image: cp.ndarray,
    text: str,
    org: cv2.typing.Point | tuple[int, int],
    font_face: int = cv2.FONT_HERSHEY_SIMPLEX,
    font_scale: float = 1.0,
    color: tuple[float, float, float] = (1.0, 1.0, 1.0),
    thickness: int = 2,
    line_type: int = cv2.LINE_AA,
    density: float = 1.0,
) -> cp.ndarray:
    """
    Draw text on an image.

    Args:
        image (cp.ndarray): The input image.
        text (str): The text to draw.
        position (tuple[int, int]): The position to draw the text.
        font_scale (float): Scale factor for the font size.
        color (tuple[int, int, int]): Color of the text in BGR format.
        thickness (int): Thickness of the text.
        font_face (int): Font type.

    Returns:
        cp.ndarray: The image with the drawn text.
    """

    original_shape = image.shape

    if density > 1.0:
        # Resize the image to reduce the density
        image = resize(image, fx=density, fy=density, interpolation=INTER_AUTO)

    _image = to_numpy(image)
    cv2.putText(
        _image,
        text=text,
        org=(int(org[0] * density), int(org[1] * density)),
        fontFace=font_face,
        fontScale=font_scale * density,
        color=color,
        thickness=int(thickness * density),
        lineType=line_type,
    )
    _image = to_cupy(_image)

    if density > 1.0:
        _image = resize(_image, dsize=(original_shape[1], original_shape[0]), interpolation=INTER_AUTO)

    return _image


def add_label(
    image: cp.ndarray,
    text: str,
    org: cv2.typing.Point | tuple[int, int] = (0, 0),
    font_face: int = cv2.FONT_HERSHEY_SIMPLEX,
    font_scale: float = 1.0,
    color: tuple[float, float, float] = (1.0, 1.0, 1.0),
    thickness: int = 2,
    line_type: int = cv2.LINE_AA,
    label_size: int = 20,
    label_color: tuple[float, float, float] = (0.0, 0.0, 0.0),
    label_align: str = "bottom",
    density: float = 1.0,
) -> cp.ndarray:
    """
    Add a label to an image.

    Args:
        image (cp.ndarray): The input image.
        text (str): The text to add as a label.
        org (cv2.typing.Point | tuple[int, int]): The position to draw the label.
        font_face (int): Font type for the label text.
        font_scale (float): Scale factor for the font size.
        color (tuple[float, float, float]): Color of the label text in BGR format.
        thickness (int): Thickness of the label text.
        line_type (int): Line type for the label text.
        label_size (int): Height of the label box in pixels.
        label_color (tuple[float, float, float]): Color of the label box in BGR format.
        label_align (str): Alignment of the label text ("top" or "bottom").
        density (float): Density factor for resizing.

    Returns:
        cp.ndarray: The image with the added label.
    """

    # expand to image shape by label_size
    label_box = cp.zeros((label_size, image.shape[1], 3), dtype=image.dtype)
    # label_box[:] = label_color  # TypeError: Unsupported type <class 'tuple'>
    # label_box[:, :] = label_color  # TypeError: Unsupported type <class 'tuple'>

    # label_color is tuple[float, float, float], Do you understand?
    label_box[:, :, 0] = label_color[0]
    label_box[:, :, 1] = label_color[1]
    label_box[:, :, 2] = label_color[2]

    label_box = put_text(
        label_box,
        text=text,
        org=(0, label_size - 5) if label_align == "bottom" else (0, 15),
        font_face=font_face,
        font_scale=font_scale,
        color=color,
        thickness=thickness,
        line_type=line_type,
        density=density,
    )
    image = cp.concatenate((image, label_box), axis=0)

    return image
