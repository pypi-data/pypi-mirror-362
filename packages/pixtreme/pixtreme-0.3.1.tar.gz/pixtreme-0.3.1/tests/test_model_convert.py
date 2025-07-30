import argparse

import pytest

import pixtreme_source as px


def test_torch_to_onnx(
    source_pth_path: str = "models/face/GFPGANv1.4.pth",
    dest_onnx_path: str = "models/face/GFPGANv1.4.fp16.onnx",
    input_shape: tuple[int, int, int, int] | None = None,
    dynamic_axes: dict | None = None,
    precision: str = "fp16",
):
    px.torch_to_onnx(
        model_path=source_pth_path,
        onnx_path=dest_onnx_path,
        input_shape=input_shape,
        dynamic_axes=dynamic_axes,
        precision=precision,
    )


def test_onnx_to_onnx(
    onnx_path: str = "models/face/GFPGANv1.4.onnx",
):
    output_path = onnx_path.replace(".onnx", ".dynamic.onnx")
    px.onnx_to_onnx_dynamic(
        input_path=onnx_path,
        output_path=output_path,
        opset=18,
    )

    px.check_onnx_model(output_path)

    import numpy as np
    import onnx
    import onnx_graphsurgeon as gs

    m = onnx.load(output_path)
    print(f"ONNX model opset version: {m.opset_import[0].version}, ir_version: {m.ir_version}")

    g = gs.import_onnx(m)
    for n in g.nodes:
        if n.op == "Div" and isinstance(n.inputs[1], gs.Constant):
            n.op = "Mul"
            n.inputs[1].values = 1.0 / n.inputs[1].values.astype(np.float32)
    g.cleanup().toposort()
    onnx.save(gs.export_onnx(g), "reswapper_fixed.onnx")

    px.onnx_to_trt_dynamic_shape(
        onnx_path="reswapper_fixed.onnx",
        engine_path="reswapper_fixed.dynamic.trt",
        batch_range=(1, 1, 512),
        spatial_range=(256, 256, 256),
        precision="tf32",
    )


if __name__ == "__main__":
    # test_torch_to_onnx()
    # test_onnx_to_onnx("models/face/reswapper-1019500.onnx")
    # test_onnx_to_onnx("models/face/reswapper_256-1567500_originalInswapperClassCompatible.onnx")
    test_onnx_to_onnx("models/face/reswapper_256.onnx")
