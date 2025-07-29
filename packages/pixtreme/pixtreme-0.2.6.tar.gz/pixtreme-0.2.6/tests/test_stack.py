import pixtreme_source as px


def test_stack():
    image_pathes = ["examples/example.png", "examples/example2.png", "examples/example3.png"]

    images = [px.imread(path) for path in image_pathes]
    stacked_image_0 = px.stack_images(images, axis=0)
    stacked_image_1 = px.stack_images(images, axis=1)

    px.imshow("axis=0", stacked_image_0)
    px.imshow("axis=1", stacked_image_1)
    px.waitkey(0)
    px.destroy_all_windows()


if __name__ == "__main__":
    test_stack()
    print("Test completed successfully.")
