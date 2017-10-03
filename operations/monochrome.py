import math


def convert_to_grayscale(image):
    for x, y in image:
        red = image.reds[x][y]
        green = image.greens[x][y]
        blue = image.blues[x][y]

        gray = math.floor(0.299 * red + 0.587 * green + 0.114 * blue)

        image.reds[x][y] = image.greens[x][y] = image.blues[x][y] = gray


if __name__ == '__main__':
    import sys
    import imageio

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else input_file

    image = imageio.read(input_file)
    convert_to_grayscale(image)
    imageio.write(image, output_file)
