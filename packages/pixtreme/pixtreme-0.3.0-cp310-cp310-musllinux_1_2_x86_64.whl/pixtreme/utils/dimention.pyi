from __future__ import annotations
import builtins as __builtins__
import cupy as cp
from pixtreme.color.bgr import bgr_to_rgb
from pixtreme.color.bgr import rgb_to_bgr
from pixtreme.transform.resize import resize
from pixtreme.utils.dtypes import to_float32
import typing
__all__ = ['INTER_AUTO', 'Layout', 'batch_to_images', 'bgr_to_rgb', 'cp', 'guess_image_layout', 'image_to_batch', 'image_to_batch_pixelshift', 'images_to_batch', 'pixelshift_fuse', 'resize', 'rgb_to_bgr', 'to_float32']
def batch_to_images(batch: cp.ndarray, scalefactor: float | None = None, mean: float | tuple[float, float, float] | None = None, swap_rb: bool = True, layout: Layout = 'NCHW') -> list[cp.ndarray]:
    """
    
        Convert a batch of images to a list of images.
    
        Args:
            batch (cp.ndarray): The input batch of images with shape (N, C, H, W) or (N, H, W, C).
    
        Returns:
            list[cp.ndarray]: A list of images, each with shape (H, W, C).
        
    """
def guess_image_layout(image: cp.ndarray) -> Layout:
    """
    
        Infer the layout of an image array.
    
        Args:
            image (cp.ndarray): The input image array.
        Returns:
            Layout: The inferred layout of the image array.
        
    """
def image_to_batch(image: cp.ndarray, scalefactor: float | None = None, size: int | tuple[int, int] | None = None, mean: float | tuple[float, float, float] | None = None, swap_rb: bool = True, layout: Layout = 'HWC') -> cp.ndarray:
    """
    
        Convert a single image to a batch.
        
    """
def image_to_batch_pixelshift(image: cp.ndarray, dim: int = 4, scalefactor: float | None = None, mean: float | tuple[float, float, float] | None = None, swap_rb: bool = True) -> cp.ndarray:
    """
    
        (H, W, C) 画像からサブピクセル位置ごとに dim² 枚を取り出し、
        (dim², C, H/dim, W/dim) の CHW テンソルを返す。
        
    """
def images_to_batch(images: cp.ndarray | list[cp.ndarray], scalefactor: float | None = None, size: int | tuple[int, int] | None = None, mean: float | tuple[float, float, float] | None = None, swap_rb: bool = True, layout: Layout = 'HWC') -> cp.ndarray:
    """
    
        Convert a list of images to batches.
        
    """
def pixelshift_fuse(preds: cp.ndarray, acc: cp.ndarray, hits: cp.ndarray, start_idx: int, dim: int) -> None:
    """
    
        128²→4×Nearest→roll→accumulate だけを行い、
        平均は最後に acc / hits で計算。
        メモリ消費は acc+hits (~ 8 MiB for dim=8) と
        バッチ分 (最大16枚) のみ。
        
    """
INTER_AUTO: int = -1
Layout: typing._LiteralGenericAlias  # value = typing.Literal['HW', 'HWC', 'CHW', 'NHWC', 'NCHW', 'ambiguous', 'unsupported']
__test__: dict = {}
