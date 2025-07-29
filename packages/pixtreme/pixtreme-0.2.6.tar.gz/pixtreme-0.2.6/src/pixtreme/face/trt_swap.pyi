from __future__ import annotations
import builtins as __builtins__
import cupy as cp
from cupyx.scipy import ndimage as ndi
from pixtreme.color.bgr import bgr_to_rgb
from pixtreme.color.bgr import rgb_to_bgr
from pixtreme.face.emap import load_emap
from pixtreme.face.schema import PxFace
from pixtreme.transform.resize import resize
from pixtreme.utils.dimention import batch_to_images
from pixtreme.utils.dimention import images_to_batch
from pixtreme.utils.dimention import images_to_batch_pixelshift
from pixtreme.utils.dimention import pixelshift_fuse
from pixtreme.utils.dtypes import to_float32
import tensorrt as trt
import typing
__all__ = ['INTER_AUTO', 'PxFace', 'TrtFaceSwap', 'batch_to_images', 'bgr_to_rgb', 'cp', 'images_to_batch', 'images_to_batch_pixelshift', 'load_emap', 'ndi', 'pixelshift_fuse', 'resize', 'rgb_to_bgr', 'to_float32', 'trt']
class TrtFaceSwap:
    def __init__(self, *, model_path: str | None = None, model_bytes: bytes | None = None, device_id: int = 0) -> None:
        ...
    def forward(self, batch: cp.ndarray, latent: cp.ndarray) -> cp.ndarray:
        ...
    def get(self, target_image: cp.ndarray | list[cp.ndarray], latent: cp.ndarray, max_batch: int = 16) -> cp.ndarray | list[cp.ndarray]:
        """
        
                Inference with TensorRT face swap model.
        
                Args:
                    target_image (cp.ndarray | list[cp.ndarray]): Input image(s) of shape (H, W, C) or list of such images.
                    latent (cp.ndarray): Latent vector of shape (1, 512).
                    max_batch (int): Maximum batch size for inference. Default is 16.
        
                
        """
    def get_subpixel(self, target_image: cp.ndarray, latent: cp.ndarray, max_batch: int = 16):
        """
        
                Inference with subpixel pixelshift.
        
                Args:
                    target_image (cp.ndarray): Input image of shape (H, W, C).
                    latent (cp.ndarray): Latent vector of shape (1, 512).
        
                Returns:
                    cp.ndarray: Output image of shape (H, W, C).
        
                Description:
                    The input image is in BGR format.
                    Input image is divided into dim² tiles of size (dim, dim).
                    Auto-calculate dim from target_image height. # dim = H // 128.
                    Forward the tiles in batches of max_batch.
                    Combine the results using pixelshift_fuse.
                    The output image is in BGR format.
                
        """
INTER_AUTO: int = -1
__test__: dict = {}
