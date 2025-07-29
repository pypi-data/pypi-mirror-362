from __future__ import annotations
import builtins as __builtins__
import cupy as cp
import onnxruntime as onnxruntime
from pixtreme.color.bgr import rgb_to_bgr
from pixtreme.transform.resize import resize
from pixtreme.utils.dimention import batch_to_images
from pixtreme.utils.dimention import images_to_batch
from pixtreme.utils.dimention import images_to_batch_pixelshift
from pixtreme.utils.dimention import pixelshift_fuse
from pixtreme.utils.dlpack import to_cupy
from pixtreme.utils.dlpack import to_numpy
from pixtreme.utils.dtypes import to_float32
import typing
__all__ = ['GFPGAN', 'INTER_AUTO', 'batch_to_images', 'cp', 'images_to_batch', 'images_to_batch_pixelshift', 'onnxruntime', 'pixelshift_fuse', 'resize', 'rgb_to_bgr', 'to_cupy', 'to_float32', 'to_numpy']
class GFPGAN:
    def __init__(self, model_file, *args, **kwargs):
        ...
    def get(self, image: cp.ndarray | list[cp.ndarray]) -> cp.ndarray | list[cp.ndarray]:
        ...
    def get_subpixel(self, image: cp.ndarray) -> cp.ndarray:
        """
        
                Apply GFPGAN to enhance the input image(s) with subpixel pixelshift.
        
                Args:
                    image (cp.ndarray | list[cp.ndarray]): Input image(s) of shape (H, W, C) or list of such images.
        
                Returns:
                    cp.ndarray | list[cp.ndarray]: Enhanced image(s).
                
        """
INTER_AUTO: int = -1
__test__: dict = {}
