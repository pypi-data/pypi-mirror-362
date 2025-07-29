import cupy as cp

from .resize import INTER_AUTO, resize


def stack_images(images: list[cp.ndarray], axis: int = 0) -> cp.ndarray:
    """
    Stack a list of images along a specified axis.

    Args:
        images (list[cp.ndarray]): List of images to stack.
        axis (int): Axis along which to stack the images. Default is 0. 0 for vertical stacking, 1 for horizontal stacking.

    Returns:
        cp.ndarray: Stacked image.
    """
    if not images:
        raise ValueError("The list of images is empty.")

    first_image_shape = images[0].shape
    # resize all images to the same height or width
    for i, img in enumerate(images):
        width = img.shape[1]
        height = img.shape[0]
        new_width = width
        new_height = height
        if axis == 0:
            if img.shape[1] != first_image_shape[1]:
                new_width = first_image_shape[1]
                new_height = int(height * new_width / width)

        elif axis == 1:
            if img.shape[0] != first_image_shape[0]:
                new_height = first_image_shape[0]
                new_width = int(width * new_height / height)
        else:
            raise ValueError("Axis must be 0 or 1.")
        images[i] = resize(img, (new_width, new_height), interpolation=INTER_AUTO)
        # print(f"Resized image {i} to shape {images[i].shape} with height {new_height} and width {new_width}")

    stacked_image = cp.concatenate(images, axis=axis)
    return stacked_image
