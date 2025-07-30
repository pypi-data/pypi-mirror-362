from .onnx_upscaler import OnnxUpscaler
from .torch_upscaler import TorchUpscaler
from .trt_upscaler import TrtUpscaler

__all__ = [
    "OnnxUpscaler",
    "TorchUpscaler",
    "TrtUpscaler",
]
