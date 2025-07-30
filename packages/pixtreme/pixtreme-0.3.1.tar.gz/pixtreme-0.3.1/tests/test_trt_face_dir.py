import argparse
import os
import timeit

import cupy as cp
import pytest

import pixtreme_source as px


@pytest.fixture
def source_image_path():
    return "examples/example2.png"


@pytest.fixture
def target_image_path():
    return "examples/target"


@pytest.fixture
def output_image_path():
    return "examples/output.png"


def test_trt_face(source_image_path: str, target_dir: str, output_dir: str, overwrite: bool = True):
    # px.onnx_to_onnx_dynamic(input_path="models/face/inswapper_128.onnx", output_path="models/face/inswapper_128.dynamic.onnx")
    # px.onnx_to_trt_dynamic_shape(
    #    onnx_path="models/face/inswapper_128.fp16.dynamic.onnx",
    #    engine_path="models/face/swap.trt",
    #    batch_range=(1, 1, 512),
    #    spatial_range=(128, 128, 128),
    #    precision="bf16",
    # )
    # exit()

    detector = px.TrtFaceDetection(model_path="models/face/detection.trt")
    print("Face detection model loaded successfully.")

    embedding = px.TrtFaceEmbedding(model_path="models/face/embedding.trt")
    print("Face embedding model loaded successfully.")

    # px.onnx_to_trt_fixed_shape(
    #    onnx_path="models/face/swap.onnx", engine_path="models/face/swap.trt", fixed_shape=(-1, 3, 128, 128)
    # )

    swapper = px.TrtFaceSwap(model_path="models/face/reswapper-1019500.dynamic.trt")
    print("Face swap model loaded successfully.")

    enhancer = px.GFPGAN(model_file="models/face/GFPGANv1.4.onnx")
    print("GFPGAN model loaded successfully.")

    # enhancer2 = px.TorchUpscaler(model_path="models/1x_Loupe_Portrait_DeJpeg_v2_net_g_318000.pth")

    # upscaler = px.TorchUpscaler(model_path="models/4xFaceUpDAT.pth")
    upscaler = px.TorchUpscaler(model_path="models/2x_Loupe_Portrait_DeJpeg_v3_net_g_214000.pth")
    print("Upscaler model loaded successfully.")

    mask = px.create_rounded_mask(dsize=(512, 512), mask_offsets=(0.2, 0.2, 0.2, 0.2), density=1, blur_size=51, sigma=16.0)
    print("Mask created successfully.")

    source_image = px.imread(source_image_path)
    source_image = px.to_float32(source_image)
    print("Source image loaded successfully.")

    source_faces = detector.get(source_image, crop_size=512)
    source_face = source_faces[0] if source_faces else None
    assert source_face is not None, "No face detected in source image."

    source_face.image = enhancer.get(source_face.image)
    source_latent = embedding.get(source_face)
    print("Source face detected and embedded successfully.")

    square_black_image = cp.zeros_like(source_face.image)

    target_pathes = []
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            # if "_shape" in file:
            #    continue
            if file.endswith((".png", ".jpg", ".jpeg")):
                target_pathes.append(os.path.join(root, file))

    for target_image_path in target_pathes:
        if not os.path.exists(target_image_path):
            raise FileNotFoundError(f"Target image not found: {target_image_path}")

        target_relative_dir = os.path.dirname(os.path.relpath(target_image_path, start=target_dir))
        output_image_dir = os.path.join(output_dir, target_relative_dir)
        os.makedirs(output_image_dir, exist_ok=True)

        source_file_name = os.path.basename(source_image_path).split(".")[0]
        target_file_name = os.path.basename(target_image_path).split(".")[0]
        output_image_path = os.path.abspath(os.path.join(output_image_dir, f"{source_file_name}_vs_{target_file_name}.png"))

        if not overwrite and os.path.exists(output_image_path):
            print(f"Output image already exists: {output_image_path}. Skipping...")
            continue

        target_image: cp.ndarray = px.imread(target_image_path)
        target_image = px.to_float32(target_image)

        if target_image.shape[0] < 768 or target_image.shape[1] < 768:
            if target_image.shape[0] < target_image.shape[1]:
                new_height = 768
                new_width = int(target_image.shape[1] * (768 / target_image.shape[0]))
                target_image = px.resize(target_image, dsize=(new_width, new_height), interpolation=px.INTER_AUTO)
            else:
                new_width = 768
                new_height = int(target_image.shape[0] * (768 / target_image.shape[1]))
                target_image = px.resize(target_image, dsize=(new_width, new_height), interpolation=px.INTER_AUTO)

        print(f"Target image size: {target_image.shape[0]}x{target_image.shape[1]}")
        print("Target image loaded successfully.")

        start = timeit.default_timer()
        pasted_image = None

        target_faces = detector.get(target_image, crop_size=512)
        target_face = target_faces[0] if target_faces else None

        if len(target_faces) == 0 or target_face is None:
            print("No face detected in target image. Skipping...")

            _sample_images = px.stack_images(
                [source_face.image, square_black_image, square_black_image, square_black_image],
                axis=0,
            )

            black_target_image = cp.zeros_like(target_image)

            _result = px.stack_images([target_image, _sample_images, black_target_image], axis=1)

            px.imwrite(output_image_path, _result)
            continue

        # target_face = embedding.get(target_face)
        print("Target face detected successfully.")

        target_face_image = target_face.image
        # target_face_image = upscaler.get(target_face_image)

        # target_face_image = enhancer.get_subpixel(target_face_image)
        # target_face_image = px.resize(target_face_image, dsize=(1024, 1024), interpolation=px.INTER_AUTO)

        swapped_face_image: cp.ndarray = swapper.get_subpixel(target_face_image, source_latent)
        print(f"Swapped face image shape: {swapped_face_image.shape}")

        swapped_face_image = enhancer.get_subpixel(swapped_face_image)
        # swapped_face_image = upscaler.get(swapped_face_image)
        assert target_face.matrix is not None, "Target face matrix is None."
        scalefactor = swapped_face_image.shape[0] / target_face.image.shape[0]

        print(f"Source face image shape: {source_face.image.shape}")
        print(f"Target face image shape: {target_face_image.shape}")
        print(f"Swapped face image shape after upscaling: {swapped_face_image.shape}")
        print(f"Scale factor: {scalefactor:.2f}")
        M = target_face.matrix * scalefactor
        pasted_image = px.paste_back(target_image=target_image, paste_image=swapped_face_image, M=M, mask=mask)
        print("Face swap completed successfully.")

        end = timeit.default_timer()
        print(f"Processed in {end - start:.2f} seconds.")

        assert pasted_image is not None, "Face swap failed."

        sample_images = px.stack_images(
            [
                source_face.image,
                target_face.image,
                target_face_image,
                swapped_face_image,
            ],
            axis=0,
        )

        result = px.stack_images([target_image, sample_images, pasted_image], axis=1)
        result = px.to_uint8(result)

        px.imwrite(output_image_path, result)
        print(f"Output image saved to {output_image_path}")
        # px.imshow("Result", result)
        # px.waitkey(1)
    px.destroy_all_windows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test TRT Face Swap")
    parser.add_argument(
        "--source",
        type=str,
        default="Z:/Projects/rashisa/00_footages/250709/member/1_Vo/IMG_0332.png",
        help="Path to the source image directory",
    )
    parser.add_argument(
        "--target_dir", type=str, default="Z:/Projects/rashisa/00_footages/250711", help="Path to the target image directory"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="Z:/Projects/rashisa/output/250711/sequence",
        help="Path to save the output image directory",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output images")
    args = parser.parse_args()

    source = os.path.abspath(args.source)
    target_dir = os.path.abspath(args.target_dir)
    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    test_trt_face(source, target_dir, output_dir, overwrite=False)

    print("Test completed successfully.")
