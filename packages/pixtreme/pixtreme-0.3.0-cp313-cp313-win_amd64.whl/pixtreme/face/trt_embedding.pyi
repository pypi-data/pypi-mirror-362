from __future__ import annotations
import builtins as __builtins__
import cupy as cp
import numpy as np
from pixtreme.face.emap import load_emap
from pixtreme.face.schema import PxFace
from pixtreme.utils.dimention import images_to_batch
import tensorrt as trt
import typing
__all__ = ['PxFace', 'TrtFaceEmbedding', 'cp', 'images_to_batch', 'load_emap', 'np', 'trt']
class TrtFaceEmbedding:
    def __init__(self, model_path: str | None = None, model_bytes: bytes | None = None, device_id: int = 0) -> None:
        """
        
                Initialize the TrtFaceEmbedding.
        
                Args:
                    model_path (str): Path to the TensorRT engine file.
                    model_bytes (bytes): TensorRT engine bytes.
                    device_id (int): CUDA device ID.
                Raises:
                    FileNotFoundError: If the specified path does not exist.
                
        """
    def forward(self, images: list[cp.ndarray] | cp.ndarray) -> cp.ndarray:
        """
        Forward pass using TensorRT
        """
    def get(self, face: PxFace) -> cp.ndarray:
        """
        Extract embedding for a single face
        """
    def initialize(self):
        """
        Initialize processing
        """
__test__: dict = {}
