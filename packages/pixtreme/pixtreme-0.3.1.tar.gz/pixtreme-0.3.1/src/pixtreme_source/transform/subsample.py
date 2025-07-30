import cupy as cp


def subsample_image(image: cp.ndarray, dim: int) -> list[cp.ndarray]:
    """Perform interleaved subsampling of an image without for loops.

    Args:
        image: Input image (cp.ndarray) with shape (height, width) or (height, width, channels).
        dim: Block size for subsampling.

    Returns:
        List of interleaved subsampled images.
    """
    # Get image dimensions
    if image.ndim == 2:
        height, width = image.shape
        channels = None
    elif image.ndim == 3:
        height, width, channels = image.shape
    else:
        raise ValueError("Image must be 2D or 3D")

    # Check if dimensions are divisible by dim
    if height % dim != 0 or width % dim != 0:
        raise ValueError(f"Image size ({height}×{width}) must be divisible by dim ({dim})")

    # Calculate new dimensions
    new_height = height // dim
    new_width = width // dim

    if channels is None:
        # For grayscale images
        # Reshape image to (new_height, dim, new_width, dim)
        reshaped = image.reshape(new_height, dim, new_width, dim)
        # Transpose axes to (dim, dim, new_height, new_width)
        transposed = reshaped.transpose(1, 3, 0, 2)
        # Reshape to (dim*dim, new_height, new_width)
        flattened = transposed.reshape(dim * dim, new_height, new_width)
        # Convert to list
        result = [flattened[i] for i in range(dim * dim)]
    else:
        # For color images
        # Reshape image to (new_height, dim, new_width, dim, channels)
        reshaped = image.reshape(new_height, dim, new_width, dim, channels)
        # Transpose axes to (dim, dim, new_height, new_width, channels)
        transposed = reshaped.transpose(1, 3, 0, 2, 4)
        # Reshape to (dim*dim, new_height, new_width, channels)
        flattened = transposed.reshape(dim * dim, new_height, new_width, channels)
        # Convert to list
        result = [flattened[i] for i in range(dim * dim)]

    return result


def subsample_image_back(subsampled_images: list[cp.ndarray], dim: int) -> cp.ndarray:
    """Reconstruct the original image from a list of subsampled images without for loops.

    Args:
        subsampled_images: List of subsampled images.
        dim: Block size used in the original subsampling.

    Returns:
        Reconstructed original image.
    """
    if len(subsampled_images) != dim * dim:
        raise ValueError(f"Incorrect number of subsampled images. Expected: {dim * dim}, Actual: {len(subsampled_images)}")

    # Get shape information from the first image
    first_image = subsampled_images[0]

    if first_image.ndim == 2:
        # For grayscale images
        sub_height, sub_width = first_image.shape
        channels = None

        # Stack all subsampled images into one tensor
        # (dim*dim, sub_height, sub_width)
        stacked = cp.stack(subsampled_images, axis=0)

        # (dim*dim, sub_height, sub_width) -> (dim, dim, sub_height, sub_width)
        reshaped = stacked.reshape(dim, dim, sub_height, sub_width)

        # (dim, dim, sub_height, sub_width) -> (sub_height, dim, sub_width, dim)
        transposed = reshaped.transpose(2, 0, 3, 1)

        # (sub_height, dim, sub_width, dim) -> (sub_height*dim, sub_width*dim)
        reconstructed = transposed.reshape(sub_height * dim, sub_width * dim)

    elif first_image.ndim == 3:
        # For color images
        sub_height, sub_width, channels = first_image.shape

        # Stack all subsampled images into one tensor
        # (dim*dim, sub_height, sub_width, channels)
        stacked = cp.stack(subsampled_images, axis=0)

        # (dim*dim, sub_height, sub_width, channels) -> (dim, dim, sub_height, sub_width, channels)
        reshaped = stacked.reshape(dim, dim, sub_height, sub_width, channels)

        # (dim, dim, sub_height, sub_width, channels) -> (sub_height, dim, sub_width, dim, channels)
        transposed = reshaped.transpose(2, 0, 3, 1, 4)

        # (sub_height, dim, sub_width, dim, channels) -> (sub_height*dim, sub_width*dim, channels)
        reconstructed = transposed.reshape(sub_height * dim, sub_width * dim, channels)

    else:
        raise ValueError("Subsampled images must be 2D or 3D")

    return reconstructed
