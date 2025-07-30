from __future__ import annotations
import builtins as __builtins__
import cupy as cp
import cv2 as cv2
from pixtreme.transform.resize import resize
from pixtreme.utils.dlpack import to_cupy
from pixtreme.utils.dlpack import to_numpy
import typing
__all__ = ['INTER_AUTO', 'add_label', 'cp', 'cv2', 'put_text', 'resize', 'to_cupy', 'to_numpy']
def add_label(image: cp.ndarray, text: str, org: cv2.typing.Point | tuple[int, int] = (0, 0), font_face: int = 0, font_scale: float = 1.0, color: tuple[float, float, float] = (1.0, 1.0, 1.0), thickness: int = 2, line_type: int = 16, label_size: int = 20, label_color: tuple[float, float, float] = (0.0, 0.0, 0.0), label_align: str = 'bottom', density: float = 1.0) -> cp.ndarray:
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
def put_text(image: cp.ndarray, text: str, org: cv2.typing.Point | tuple[int, int], font_face: int = 0, font_scale: float = 1.0, color: tuple[float, float, float] = (1.0, 1.0, 1.0), thickness: int = 2, line_type: int = 16, density: float = 1.0) -> cp.ndarray:
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
INTER_AUTO: int = -1
__test__: dict = {}
