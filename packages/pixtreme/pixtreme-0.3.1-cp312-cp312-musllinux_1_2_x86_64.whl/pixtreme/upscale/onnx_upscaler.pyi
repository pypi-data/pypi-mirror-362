from __future__ import annotations
import builtins as __builtins__
import cupy as cp
import onnxruntime as onnxruntime
import typing
__all__ = ['OnnxUpscaler', 'cp', 'onnxruntime']
class OnnxUpscaler:
    """
    ONNX-based image upscaler with CUDA and CPU provider support.
    
        This class provides optimized inference for ONNX upscaling models with automatic
        fallback handling for type inconsistencies and efficient memory management.
        
    """
    def __init__(self, model_path: str | None = None, model_bytes: bytes | None = None, device_id: int = 0, provider_options: list | None = None) -> None:
        """
        Initialize the ONNX upscaler.
        
                Args:
                    model_path: Path to the ONNX model file. Either this or model_bytes must be provided.
                    model_bytes: Raw bytes of the ONNX model. Either this or model_path must be provided.
                    device_id: CUDA device ID to use for inference.
                    provider_options: Custom provider options for ONNX Runtime.
        
                Raises:
                    ValueError: If neither model_path nor model_bytes is provided.
                    RuntimeError: If ONNX model cannot be loaded due to type inconsistencies.
                
        """
    def _ensure_buffers(self, input_shape):
        """
        Ensure necessary buffers are allocated for the given input shape.
        
                Args:
                    input_shape: Shape of the input image as (height, width, channels).
                
        """
    def get(self, image: cp.ndarray) -> cp.ndarray:
        """
        Internal method to perform upscaling on a single image.
        
                Args:
                    image: Single image array to upscale.
        
                Returns:
                    Upscaled image array.
                
        """
    def post_process(self, output_frame: cp.ndarray) -> cp.ndarray:
        """
        Post-process ONNX inference output.
        
                Converts from NCHW to HWC format and RGB back to BGR.
        
                Args:
                    output_frame: Model output in NCHW format.
        
                Returns:
                    Post-processed image array in HWC BGR format.
                
        """
    def pre_process(self, input_frame: cp.ndarray) -> cp.ndarray:
        """
        Preprocess input frame for ONNX inference.
        
                Converts BGR to RGB, handles different channel configurations,
                and transforms from HWC to NCHW format.
        
                Args:
                    input_frame: Input image array in HWC format.
        
                Returns:
                    Preprocessed image array in NCHW format ready for inference.
                
        """
__test__: dict = {}
