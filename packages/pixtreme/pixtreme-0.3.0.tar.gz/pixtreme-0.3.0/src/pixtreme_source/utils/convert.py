import os
import sys
from itertools import chain

import onnx
import onnx.shape_inference
import onnx_graphsurgeon as gs
import spandrel_extra_arches as ex_arch
import tensorrt as trt
import torch
from onnx.version_converter import convert_version
from spandrel import ModelDescriptor, ModelLoader


def onnx_to_onnx_dynamic(input_path: str, output_path: str, opset: int | None = None, irver: int | None = None) -> None:
    m = onnx.load(input_path)

    # --- Rewrite batch dimension (1→-1) ---------------------------
    for v in chain(m.graph.input, m.graph.output):
        v.type.tensor_type.shape.dim[0].dim_param = "N"

    # --- Shape inference → minimal optimization ----------------------------
    m = onnx.shape_inference.infer_shapes(m)
    g = gs.import_onnx(m).toposort().cleanup()
    m2 = gs.export_onnx(g)

    if opset is not None:
        m2 = convert_version(m2, opset)
    else:
        if m2.opset_import[0].version > 19:
            m2 = convert_version(m2, 19)
        m2.opset_import[0].version = 19

    if irver is not None:
        m2.ir_version = irver
    else:
        if m2.ir_version > 10:
            m2.ir_version = 10
        m2.ir_version = 10

    print(f"Exporting ONNX model to dynamic shape: {input_path} → {output_path}")
    print(f"Opset version: {m2.opset_import[0].version}")
    print(f"IR version: {m2.ir_version}")
    print(f"Graph inputs: {[i.name for i in m2.graph.input]}")
    print(f"Graph outputs: {[o.name for o in m2.graph.output]}")

    # --- Final check -------------------------------------------
    onnx.checker.check_model(m2)
    onnx.save(m2, output_path)

    print(f"✅ ONNX model exported to: {output_path}")


def check_torch_model(model_path: str) -> None:
    """check_torch_model
    Check if the PyTorch model file exists and is valid, and analyze input constraints.

    Args:
        model_path: Path to the PyTorch model file (.pth or .pt)
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    try:
        ex_arch.install()
        model_desc: ModelDescriptor = ModelLoader().load_from_file(model_path)
        print(f"✅ Valid PyTorch model found at: {model_path}")

        # Architecture information
        print(f"\n🏗️ Architecture: {model_desc.architecture.name}")
        print(f"   ID: {model_desc.architecture.id}")
        print(f"   Purpose: {model_desc.purpose}")

        # Model properties
        print("\n📊 Model Properties:")
        print(f"   Scale: {model_desc.scale}x")
        print(f"   Input channels: {model_desc.input_channels}")
        print(f"   Output channels: {model_desc.output_channels}")
        print(f"   Tiling support: {model_desc.tiling.name}")

        # Precision support
        print("\n🎯 Precision Support:")
        print(f"   FP16: {'✅' if model_desc.supports_half else '❌'}")
        print(f"   BF16: {'✅' if model_desc.supports_bfloat16 else '❌'}")
        print("   FP32: ✅")

        # Size requirements analysis
        size_req = model_desc.size_requirements
        print("\n📏 Size Requirements:")
        print(f"   Minimum size: {size_req.minimum} pixels")
        print(f"   Multiple of: {size_req.multiple_of}")
        print(f"   Square required: {'✅' if size_req.square else '❌'}")

        if size_req.none:
            print("   🔄 No specific size constraints")
        else:
            print("   ⚠️ Has size constraints")

        # Calculate recommended input size ranges
        print("\n🎯 Recommended Input Size Ranges:")

        # Calculate minimum size
        min_size = max(64, size_req.minimum)
        if size_req.multiple_of > 1:
            min_size = ((min_size - 1) // size_req.multiple_of + 1) * size_req.multiple_of

        # Calculate optimal sizes
        optimal_sizes = [512, 768, 1024]
        valid_optimal = []
        for size in optimal_sizes:
            adjusted = size
            if size_req.multiple_of > 1:
                adjusted = ((size - 1) // size_req.multiple_of + 1) * size_req.multiple_of
            if adjusted >= size_req.minimum:
                valid_optimal.append(adjusted)

        # Calculate maximum size
        max_size = 4096
        if size_req.multiple_of > 1:
            max_size = (max_size // size_req.multiple_of) * size_req.multiple_of

        print(f"   Minimum: {min_size}x{min_size}")
        print(f"   Optimal: {', '.join([f'{s}x{s}' for s in valid_optimal[:3]])}")
        print(f"   Maximum: {max_size}x{max_size} (practical limit)")

        if size_req.square:
            print("   ⚠️ Model requires square input (width == height)")

        # Tiling recommendations
        print("\n🧩 Tiling Recommendations:")
        if model_desc.tiling.name == "SUPPORTED":
            print("   ✅ Tiling supported - safe for large images")
            print("   💡 Recommended tile size: 512x512 to 1024x1024")
        elif model_desc.tiling.name == "DISCOURAGED":
            print("   ⚠️ Tiling discouraged - may cause artifacts")
            print("   💡 Use smaller images or full-size processing")
        elif model_desc.tiling.name == "INTERNAL":
            print("   🔄 Model handles tiling internally")
            print("   💡 Do not tile externally - process full images")

        # Recommended settings for ONNX conversion
        print("\n🚀 ONNX Export Recommendations:")
        recommended_shape = (
            1,
            model_desc.input_channels,
            valid_optimal[0] if valid_optimal else min_size,
            valid_optimal[0] if valid_optimal else min_size,
        )
        print(f"   Recommended input_shape: {recommended_shape}")
        print("   Dynamic axes suggested for flexible sizing")

        # Tags information
        if model_desc.tags:
            print(f"\n🏷️ Model Tags: {', '.join(model_desc.tags)}")

    except Exception as e:
        raise RuntimeError(f"Failed to load PyTorch model: {e}")


def check_onnx_model(model_path: str) -> None:
    """check_onnx_model
    Check if the ONNX model file exists and is valid, and show dynamic input constraints.

    Args:
        model_path: Path to the ONNX model file (.onnx)
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"ONNX model file not found: {model_path}")

    try:
        model = onnx.load(model_path)
        onnx.checker.check_model(model)
        print(f"✅ Valid ONNX model found at: {model_path}")

        print(f"\n🏗️ ONNX Model Architecture: {model.opset_import[0].domain} v{model.opset_import[0].version}")
        print(f"   IR Version: {model.ir_version}")
        print(f"   Producer: {model.producer_name} v{model.producer_version}")
        print(f"   Model Version: {model.model_version}")
        print(f"   Domain: {model.domain}")

        # Input information analysis
        for i, input_info in enumerate(model.graph.input):
            print(f"\n📥 Input {i}: {input_info.name}")
            print(f"   Data Type: {onnx.TensorProto.DataType.Name(input_info.type.tensor_type.elem_type)}")

            # Analyze input shape
            shape_info = input_info.type.tensor_type.shape
            shape_str = []
            dynamic_dims = []

            for dim_idx, dim in enumerate(shape_info.dim):
                if dim.HasField("dim_value"):
                    # Fixed size
                    shape_str.append(str(dim.dim_value))
                elif dim.HasField("dim_param"):
                    # Dynamic size by parameter name
                    shape_str.append(f"{dim.dim_param}")
                    dynamic_dims.append((dim_idx, dim.dim_param))
                else:
                    # Unconstrained dynamic size
                    shape_str.append("?")
                    dynamic_dims.append((dim_idx, "unconstrained"))

            print(f"   Shape: [{', '.join(shape_str)}]")

            if dynamic_dims:
                print(f"   🔄 Dynamic dimensions: {len(dynamic_dims)} found")
                for dim_idx, dim_name in dynamic_dims:
                    print(f"      Axis {dim_idx}: {dim_name}")

                    # Infer constraint information (common patterns)
                    if dim_idx == 0:
                        print("         💡 Likely batch dimension (typical range: 1-16)")
                    elif dim_idx == 1:
                        print("         💡 Likely channel dimension (typically fixed)")
                    elif dim_idx >= 2:
                        print("         💡 Likely spatial dimension (height/width)")
                        print("            🔍 Common ranges for upscaling models:")
                        print("               Min: 64-128 pixels")
                        print("               Max: 2048-8192 pixels")
                        print("               Optimal: 512-1024 pixels")
            else:
                print("   📏 Static shape (no dynamic dimensions)")

        # Output information analysis
        for i, output_info in enumerate(model.graph.output):
            print(f"\n📤 Output {i}: {output_info.name}")
            print(f"   Data Type: {onnx.TensorProto.DataType.Name(output_info.type.tensor_type.elem_type)}")

            # Analyze output shape
            shape_info = output_info.type.tensor_type.shape
            shape_str = []

            for dim in shape_info.dim:
                if dim.HasField("dim_value"):
                    shape_str.append(str(dim.dim_value))
                elif dim.HasField("dim_param"):
                    shape_str.append(f"{dim.dim_param}")
                else:
                    shape_str.append("?")

            print(f"   Shape: [{', '.join(shape_str)}]")

        # TensorRT engine creation recommendations
        print("\n🚀 TensorRT optimization profile recommendations:")
        print("   For dynamic models, consider using these typical ranges:")
        print("   - Batch size: min=1, opt=1, max=4")
        print("   - Height/Width: min=256, opt=512, max=2048")
        print("   - Use onnx_to_trt_dynamic_shape() for dynamic input handling")

    except Exception as e:
        raise RuntimeError(f"Failed to load ONNX model: {e}")


def check_trt_model(
    engine_path: str,
    verbose: bool = False,
) -> None:
    print(f"Checking TensorRT model: {engine_path}")
    if not os.path.exists(engine_path):
        raise FileNotFoundError(f"{engine_path} does not exist")

    with open(engine_path, "rb") as f:
        model_bytes = f.read()

    logger = trt.Logger(trt.Logger.WARNING)
    runtime = trt.Runtime(logger)
    engine = runtime.deserialize_cuda_engine(model_bytes)
    engine.create_execution_context()

    for name in engine:
        input_shape = engine.get_tensor_shape(name)
        input_dtype = engine.get_tensor_dtype(name)
        print(f"Input: Tensor: {name}, Shape: {input_shape}, Type: {trt.nptype(input_dtype)}")


def torch_to_onnx(
    model_path: str,
    onnx_path: str,
    input_shape: tuple | None = None,
    dynamic_axes: dict | None = None,
    opset_version: int = 20,
    precision: str = "fp32",
    device: str = "cuda",
) -> None:
    """torch_to_onnx
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
    print(f"Exporting PyTorch model to ONNX: {model_path} → {onnx_path}")
    print(f"Precision: {precision}, Device: {device}")
    ex_arch.install()

    model = ModelLoader().load_from_file(model_path).model.to(torch.device(device)).eval()

    if precision == "fp16":
        dtype = torch.float16
    elif precision == "bf16":
        dtype = torch.bfloat16
    else:
        dtype = torch.float32

    if dynamic_axes is None and input_shape is None:
        dynamic_axes = {
            "input": {0: "batch_size", 2: "height", 3: "width"},
            "output": {0: "batch_size", 2: "height", 3: "width"},
        }

    if input_shape is None:
        input_shape = (1, 3, 128, 128)

    print(f"Input shape: {input_shape}")
    print(f"Dynamic axes: {dynamic_axes}")

    # Use autocast for precision control (reverting to original behavior)
    with torch.autocast(device, dtype=dtype):
        dummy_input = torch.randn(input_shape, device=device)
        try:
            torch.onnx.export(
                model,
                (dummy_input,),
                onnx_path,
                opset_version=opset_version,
                export_params=True,
                do_constant_folding=True,
                input_names=["input"],
                output_names=["output"],
                dynamic_axes=dynamic_axes,
                optimize=True,
            )
            print(f"✅ ONNX model exported to: {onnx_path}")

        except Exception as e:
            print(f"❌ ONNX export failed: {e}")
            if "fp16" in precision.lower() or "half" in str(e).lower():
                print("💡 Suggestion: Try exporting with fp32 precision to avoid type issues")
                print("   Use precision='fp32' parameter")
            raise


def onnx_to_trt_dynamic_shape(
    onnx_path: str,
    engine_path: str,
    *,
    precision: str = "fp16",
    workspace: int = 1024 << 20,  # 1024 MiB
    batch_range: tuple[int, int, int] = (1, 1, 16),  # (min,opt,max) for axis-0 if dynamic
    spatial_range: tuple[int, int, int] = (64, 128, 512),  # (min,opt,max) for H/W if dynamic
    verbose: bool = False,
) -> None:
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
    print("------------------ ONNX to TensorRT Dynamic Shape Conversion -----------------")
    print(f"Building TensorRT engine from ONNX model: {onnx_path}")
    if not os.path.exists(onnx_path):
        raise FileNotFoundError(f"{onnx_path} does not exist")

    log_level = trt.Logger.INFO if verbose else trt.Logger.WARNING
    logger = trt.Logger(log_level)
    builder = trt.Builder(logger)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    parser = trt.OnnxParser(network, logger)

    # ----------------- Parse ONNX -----------------
    with open(onnx_path, "rb") as f:
        if not parser.parse(f.read()):
            for i in range(parser.num_errors):
                print(parser.get_error(i), file=sys.stderr)
            raise RuntimeError("Failed to parse ONNX model")

        m = onnx.load(onnx_path)
        print(f"ONNX model opset version: {m.opset_import[0].version}, ir_version: {m.ir_version}")
        print(f"ONNX model inputs: {[i.name for i in m.graph.input]}")
        print(f"ONNX model outputs: {[o.name for o in m.graph.output]}")
        print(f"ONNX model nodes: {len(m.graph.node)}")
        print(f"ONNX model initializers: {[i.name for i in m.graph.initializer]}")
        print(f"ONNX model ops: {[n.op_type for n in m.graph.node]}")

    # ----------------- Build-time flags -----------------
    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, workspace)

    precision = precision.lower()
    if precision == "fp16" and builder.platform_has_fast_fp16:
        config.set_flag(trt.BuilderFlag.FP16)
    elif precision == "bf16" and builder.platform_has_fast_fp16:
        config.set_flag(trt.BuilderFlag.BF16)
    elif precision == "int8" and builder.platform_has_fast_int8:
        config.set_flag(trt.BuilderFlag.INT8)
    else:
        # fall back to tf32 (on Ampere+) or fp32
        config.set_flag(trt.BuilderFlag.TF32)

    # ----------------- Optimisation profile -----------------
    profile = builder.create_optimization_profile()

    def _pretty(t: trt.ITensor) -> str:
        return f"{t.name:15s}  {list(t.shape)}  {t.dtype}"

    print("⇢ Inputs:")
    for idx in range(network.num_inputs):
        t = network.get_input(idx)
        print("  ", _pretty(t))

        shape_min, shape_opt, shape_max = [], [], []

        for axis, dim in enumerate(t.shape):
            if dim != -1:
                # static dimension
                d = int(dim)
                shape_min.append(d)
                shape_opt.append(d)
                shape_max.append(d)
                continue

            # dynamic dimension
            if axis == 0:  # batch
                mn, op, mx = batch_range
            elif axis >= 2:  # assume H/W or sequence length
                mn, op, mx = spatial_range
            else:
                # dynamic channel or unknown → keep small
                mn, op, mx = (1, 1, 4)

            shape_min.append(int(mn))
            shape_opt.append(int(op))
            shape_max.append(int(mx))

        profile.set_shape(t.name, tuple(shape_min), tuple(shape_opt), tuple(shape_max))

    config.add_optimization_profile(profile)

    # ----------------- Build engine -----------------
    print("⇢ Building TensorRT engine …")
    engine_bytes = builder.build_serialized_network(network, config)
    if engine_bytes is None:
        raise RuntimeError("TensorRT engine build failed.")

    os.makedirs(os.path.dirname(engine_path) or ".", exist_ok=True)
    with open(engine_path, "wb") as f:
        f.write(engine_bytes)

    print(f"✓ Engine written to {engine_path}")


def onnx_to_trt_fixed_shape(
    onnx_path: str,
    engine_path: str,
    input_shape: tuple = (1, 3, 512, 512),
    precision: str = "fp16",
    workspace: int = 1024 << 20,
) -> None:
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

    print(f"Building TensorRT engine with fixed shape from ONNX model: {onnx_path}")
    print(f"Fixed input shape: {input_shape}")

    # Load and modify ONNX model to fix input shape
    model = onnx.load(onnx_path)

    # Get the input tensor info
    input_info = model.graph.input[0]
    original_shape = [dim.dim_value if dim.dim_value > 0 else -1 for dim in input_info.type.tensor_type.shape.dim]

    print(f"Original ONNX input shape: {original_shape}")

    # Create new input with fixed shape
    input_info.type.tensor_type.ClearField("shape")
    for dim_size in input_shape:
        dim = input_info.type.tensor_type.shape.dim.add()
        dim.dim_value = int(dim_size)

    print(f"Modified ONNX input to fixed shape: {input_shape}")

    # Validate the modified model
    try:
        onnx.checker.check_model(model)
        print("✓ Modified ONNX model is valid")
    except Exception as e:
        print(f"⚠ ONNX model validation warning: {e}")

    # Convert modified ONNX to TensorRT
    logger = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(logger)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    parser = trt.OnnxParser(network, logger)

    # Parse the modified ONNX model
    if not parser.parse(model.SerializeToString()):
        for i in range(parser.num_errors):
            print(parser.get_error(i), file=sys.stderr)
        raise RuntimeError("Failed to parse the modified ONNX model")

    # Verify input shape
    input_tensor = network.get_input(0)
    print(f"TensorRT input tensor name: {input_tensor.name}")
    print(f"TensorRT input shape: {input_tensor.shape}")

    # BuilderConfig
    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, workspace)
    if precision == "fp16" and builder.platform_has_fast_fp16:
        config.set_flag(trt.BuilderFlag.FP16)
    elif precision == "int8" and builder.platform_has_fast_int8:
        config.set_flag(trt.BuilderFlag.INT8)

    # No optimization profile needed for fixed shapes
    print("Using fixed shape - no optimization profile required")

    # Build engine
    engine_bytes = builder.build_serialized_network(network, config)
    if engine_bytes is None:
        raise RuntimeError("Engine build failed")

    with open(engine_path, "wb") as f:
        f.write(engine_bytes)

    if not os.path.exists(engine_path):
        raise RuntimeError(f"Failed to save TensorRT engine to {engine_path}")

    print(f"✅ TensorRT engine with fixed shape saved to: {engine_path}")


def onnx_to_trt(
    onnx_path: str,
    engine_path: str,
    input_shape: tuple | None = None,
    precision: str = "fp16",
    workspace: int = 512 << 20,
    spatial_range: tuple = (16, 512, 2048),
    batch_range: tuple = (1, 1, 1),
) -> None:
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
    print(f"Converting ONNX to TensorRT: {onnx_path} → {engine_path}")

    # If input_shape is provided, use fixed shape mode
    if input_shape is not None:
        print(f"🔒 Using FIXED shape mode: {input_shape}")
        print("⚠️  WARNING: Fixed shape may not work with Transformer-based models")

        # Fixed shape TensorRT conversion
        try:
            onnx_to_trt_fixed_shape(
                onnx_path=onnx_path, engine_path=engine_path, input_shape=input_shape, precision=precision, workspace=workspace
            )
        except Exception as e:
            print(f"\n❌ Fixed shape conversion failed: {e}")
            print("💡 Suggestion: Try dynamic shape mode instead")
            print("   Remove input_shape parameter or set it to None")
            raise
    else:
        print("🔄 Using DYNAMIC shape mode")
        print("⚠️  WARNING: Transformer-based models may not be compatible with TensorRT")

        # Dynamic shape TensorRT conversion
        try:
            onnx_to_trt_dynamic_shape(
                onnx_path=onnx_path,
                engine_path=engine_path,
                precision=precision,
                workspace=workspace,
                spatial_range=spatial_range,
                batch_range=batch_range,
            )
        except Exception as e:
            print(f"\n❌ Dynamic shape conversion failed: {e}")
            print("💡 Suggestion: Try fixed shape mode instead")
            print("   Use input_shape=(1, 3, 512, 512) for example")
            raise

    # Final message on success
    print("\n✅ TensorRT conversion completed successfully!")
    print(f"   Engine saved to: {engine_path}")
    print(f"   Mode: {'Fixed' if input_shape else 'Dynamic'} shape")
    print(f"   Precision: {precision}")
    print(f"   Workspace: {workspace // 1024 // 1024}MB")
