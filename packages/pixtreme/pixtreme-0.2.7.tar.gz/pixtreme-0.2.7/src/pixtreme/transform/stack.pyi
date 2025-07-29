from __future__ import annotations
import builtins as __builtins__
import cupy as cp
from pixtreme.transform.resize import resize
__all__ = ['INTER_AUTO', 'cp', 'resize', 'stack_images']
def stack_images(images: list[cp.ndarray], axis: int = 0) -> cp.ndarray:
    """
    
        Stack a list of images along a specified axis.
    
        Args:
            images (list[cp.ndarray]): List of images to stack.
            axis (int): Axis along which to stack the images. Default is 0. 0 for vertical stacking, 1 for horizontal stacking.
    
        Returns:
            cp.ndarray: Stacked image.
        
    """
INTER_AUTO: int = -1
__test__: dict = {}
