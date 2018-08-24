from color.grayscale import GrayscaleMatrix


def convert_to_grayscale(image):
    matrix = GrayscaleMatrix.from_image(image)
    matrix.apply_to(image)


if __name__ == '__main__':
    import sys
    import imageio

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else input_file

    image = imageio.read(input_file)
    convert_to_grayscale(image)
    imageio.write(image, output_file)
