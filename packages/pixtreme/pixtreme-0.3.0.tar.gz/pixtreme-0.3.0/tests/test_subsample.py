import timeit

import cupy as cp

import pixtreme_source as px

itr = 100


def test_subsample_image(image_path: str, dim: int):
    print(f"Testing subsample_image with dim={dim} on image: {image_path}")

    upscaler = px.TorchUpscaler(model_path="models/2x_Loupe_Portrait_DeJpeg_v3_net_g_214000.pth")

    test_image = px.imread(image_path)
    test_image = px.to_float32(test_image)  # float32に変換

    print(f"Original image shape: {test_image.shape}")
    print(f"Original image dtype: {test_image.dtype}")
    px.imshow("Original Image", test_image)

    results = []

    start = timeit.default_timer()
    for _ in range(itr):
        results = px.subsample_image(test_image, dim=dim)
    end = timeit.default_timer()
    print(f"Subsampled image (reshape) time: {end - start:.4f} seconds")
    print(f"Subsampled images time per iteration: {(end - start) / itr:.4f} seconds")

    print(f"Subsampled images count: {len(results)}")

    for i, subsampled in enumerate(results):
        print(f"Subsampled image {i} shape: {subsampled.shape}")
        print(f"Subsampled image {i} dtype: {subsampled.dtype}")
        px.imshow(f"Subsampled Image{i}", subsampled)
        results[i] = upscaler.get(subsampled)

    reconstructed_image = px.subsample_image_back(results, dim=dim)
    print(f"Reconstructed image shape: {reconstructed_image.shape}")
    print(f"Reconstructed image dtype: {reconstructed_image.dtype}")

    scaled_image = px.resize(
        reconstructed_image,
        (reconstructed_image.shape[1] // dim, reconstructed_image.shape[0] // dim),
        interpolation=px.INTER_AREA,
    )
    print(f"Scaled image shape: {scaled_image.shape}")
    print(f"Scaled image dtype: {scaled_image.dtype}")

    px.imshow("Reconstructed Image", reconstructed_image)
    px.imshow("Reconstructed Scaled Image", scaled_image)

    px.waitkey(0)  # Wait for a key press to close the images
    px.destroy_all_windows()  # Close all image windows


if __name__ == "__main__":
    test_subsample_image("examples/example.png", dim=2)
