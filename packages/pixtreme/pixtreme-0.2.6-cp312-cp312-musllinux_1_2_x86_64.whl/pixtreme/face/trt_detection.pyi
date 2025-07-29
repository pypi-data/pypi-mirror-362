from __future__ import annotations
import builtins as __builtins__
import cupy as cp
import numpy as np
from pixtreme.color.bgr import bgr_to_rgb
from pixtreme.color.bgr import rgb_to_bgr
from pixtreme.face.schema import PxFace
from pixtreme.transform.affine import crop_from_kps
from pixtreme.transform.resize import resize
from pixtreme.utils.blob import to_blob
from pixtreme.utils.dimention import batch_to_images
from pixtreme.utils.dimention import images_to_batch
from pixtreme.utils.dlpack import to_cupy
from pixtreme.utils.dlpack import to_numpy
from pixtreme.utils.dtypes import to_float32
import tensorrt as trt
import typing
__all__ = ['INTER_AUTO', 'PxFace', 'TrtFaceDetection', 'batch_to_images', 'bgr_to_rgb', 'cp', 'crop_from_kps', 'images_to_batch', 'np', 'resize', 'rgb_to_bgr', 'to_blob', 'to_cupy', 'to_float32', 'to_numpy', 'trt']
class TrtFaceDetection:
    def __init__(self, model_path: str | None = None, model_bytes: bytes | None = None, device_id: int = 0) -> None:
        """
        
                Initialize the TrtFaceDetection.
        
                Args:
                    model_path (str): Path to the TensorRT engine file.
                    model_bytes (bytes): TensorRT engine bytes.
                    device_id (int): CUDA device ID.
                Raises:
                    FileNotFoundError: If the specified path does not exist.
                
        """
    def crop(self, image: cp.ndarray, kps: cp.ndarray, size: int = 512) -> tuple[cp.ndarray, cp.ndarray]:
        """
        Crop face image using keypoints
        """
    def distance2bbox(self, points: cp.ndarray, distance: cp.ndarray, max_shape = None) -> cp.ndarray:
        """
        Convert distance predictions to bounding boxes
        """
    def distance2kps(self, points: cp.ndarray, distance: cp.ndarray, max_shape = None) -> cp.ndarray:
        """
        Convert distance predictions to keypoints
        """
    def forward(self, det_image: cp.ndarray, threshold: float):
        """
        Forward pass using TensorRT
        """
    def get(self, image: cp.ndarray, crop_size: int = 512, max_num: int = 0, metric: str = 'default') -> list[PxFace]:
        """
        Main detection method with the same interface as original FaceDetection
        """
    def initialize(self):
        """
        Initialize processing
        """
    def nms(self, dets: cp.ndarray):
        """
        Non-Maximum Suppression
        """
INTER_AUTO: int = -1
__test__: dict = {}
