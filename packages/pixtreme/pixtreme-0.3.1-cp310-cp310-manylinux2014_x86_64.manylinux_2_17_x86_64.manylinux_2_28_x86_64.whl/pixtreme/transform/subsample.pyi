from __future__ import annotations
import builtins as __builtins__
import cupy as cp
__all__ = ['cp', 'subsample_image', 'subsample_image_back']
def subsample_image(image: cp.ndarray, dim: int) -> list[cp.ndarray]:
    """
    Perform interleaved subsampling of an image without for loops.
    
        Args:
            image: Input image (cp.ndarray) with shape (height, width) or (height, width, channels).
            dim: Block size for subsampling.
    
        Returns:
            List of interleaved subsampled images.
        
    """
def subsample_image_back(subsampled_images: list[cp.ndarray], dim: int) -> cp.ndarray:
    """
    Reconstruct the original image from a list of subsampled images without for loops.
    
        Args:
            subsampled_images: List of subsampled images.
            dim: Block size used in the original subsampling.
    
        Returns:
            Reconstructed original image.
        
    """
__test__: dict = {}
