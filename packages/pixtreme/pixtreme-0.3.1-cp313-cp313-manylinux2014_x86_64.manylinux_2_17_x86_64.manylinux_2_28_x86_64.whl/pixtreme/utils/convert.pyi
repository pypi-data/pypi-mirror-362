from __future__ import annotations
import builtins as __builtins__
from itertools import chain
import onnx as onnx
from onnx.version_converter import convert_version
import onnx_graphsurgeon as gs
import os as os
from spandrel.__helpers.loader import ModelLoader
import spandrel_extra_arches as ex_arch
import sys as sys
import tensorrt as trt
import torch as torch
import typing
__all__ = ['ModelDescriptor', 'ModelLoader', 'chain', 'check_onnx_model', 'check_torch_model', 'check_trt_model', 'convert_version', 'ex_arch', 'gs', 'onnx', 'onnx_to_onnx_dynamic', 'onnx_to_trt', 'onnx_to_trt_dynamic_shape', 'onnx_to_trt_fixed_shape', 'os', 'sys', 'torch', 'torch_to_onnx', 'trt']
def check_onnx_model(model_path: str) -> None:
    """
    check_onnx_model
        Check if the ONNX model file exists and is valid, and show dynamic input constraints.
    
        Args:
            model_path: Path to the ONNX model file (.onnx)
        
    """
def check_torch_model(model_path: str) -> None:
    """
    check_torch_model
        Check if the PyTorch model file exists and is valid, and analyze input constraints.
    
        Args:
            model_path: Path to the PyTorch model file (.pth or .pt)
        
    """
def check_trt_model(engine_path: str, verbose: bool = False) -> None:
    ...
def onnx_to_onnx_dynamic(input_path: str, output_path: str, opset: int | None = None, irver: int | None = None) -> None:
    ...
def onnx_to_trt(onnx_path: str, engine_path: str, input_shape: tuple | None = None, precision: str = 'fp16', workspace: int = 536870912, spatial_range: tuple = (16, 512, 2048), batch_range: tuple = (1, 1, 1)) -> None:
    """
    
        Convert ONNX model to TensorRT engine with automatic dynamic/fixed shape handling.
    
        This function automatically chooses between dynamic and fixed shape optimization
        based on the provided parameters, similar to torch_to_onnx.
    
        Args:
            onnx_path: Path to input ONNX model
            engine_path: Path to output TensorRT engine
            input_shape: Fixed input shape (batch, channels, height, width). If None, uses dynamic shape.
            dynamic_axes: Dictionary defining dynamic axes (ignored if input_shape is provided)
            precision: Precision mode ('fp16', 'fp32', 'bf16', 'int8')
            workspace: Workspace size in bytes
            size_requirements: Tuple of (min_size, opt_size, max_size) for dynamic spatial dimensions
            batch_requirements: Tuple of (min_batch, opt_batch, max_batch) for dynamic batch dimension
        
    """
def onnx_to_trt_dynamic_shape(onnx_path: str, engine_path: str, *, precision: str = 'fp16', workspace: int = 1073741824, batch_range: tuple[int, int, int] = (1, 1, 16), spatial_range: tuple[int, int, int] = (64, 128, 512), verbose: bool = False) -> None:
    """
    
        Generic ONNX→TensorRT converter with *one* optimisation profile that covers
        ALL dynamic inputs (both batch & spatial dims).  Suitable for inswapper128,
        but also SwinIR, ESRGAN, or arbitrary CNNs.
    
        Parameters
        ----------
        onnx_path      : Path to .onnx network
        engine_path    : Where to write the serialized .trt engine
        precision      : 'fp32' | 'tf32' | 'fp16' | 'bf16' | 'int8'
        workspace      : Workspace size in bytes
        batch_range    : Tuple (min,opt,max) applied to **axis-0** when it is -1
        spatial_range  : Tuple (min,opt,max) applied to H/W (axes ≥2) when they are -1
        verbose        : If True, TensorRT logger prints INFO messages
        
    """
def onnx_to_trt_fixed_shape(onnx_path: str, engine_path: str, input_shape: tuple = (1, 3, 512, 512), precision: str = 'fp16', workspace: int = 1073741824) -> None:
    """
    
        Convert ONNX model to TensorRT engine with fixed input shape.
        This function first modifies the ONNX model to have fixed dimensions,
        then converts it to TensorRT for optimized performance.
    
        Args:
            onnx_path: Path to input ONNX model
            engine_path: Path to output TensorRT engine
            fixed_shape: Fixed input shape (batch, channels, height, width)
            precision: Precision mode ('fp16', 'fp32', 'int8')
            workspace: Workspace size in bytes
        
    """
def torch_to_onnx(model_path: str, onnx_path: str, input_shape: tuple | None = None, dynamic_axes: dict | None = None, opset_version: int = 20, precision: str = 'fp32', device: str = 'cuda') -> None:
    """
    torch_to_onnx
        Export a PyTorch model to ONNX format with improved type consistency.
    
        Args:
            model_path: Path to the PyTorch model file (.pth or .pt)
            onnx_path: Path to save the exported ONNX model
            input_shape: Shape of the input tensor (batch_size, channels, height, width)
            dynamic_axes: Dictionary defining dynamic axes for input and output tensors
            opset_version: ONNX opset version to use (default is 20)
            precision: Precision mode for the model ('fp16', 'bf16', 'fp32')
            device: Device to run the model on ('cuda' or 'cpu'). if VRAM is not enough, use 'cpu' to export the model.
        
    """
ModelDescriptor: typing._UnionGenericAlias  # value = typing.Union[spandrel.__helpers.model_descriptor.ImageModelDescriptor[torch.nn.modules.module.Module], spandrel.__helpers.model_descriptor.MaskedImageModelDescriptor[torch.nn.modules.module.Module]]
__test__: dict = {}
