import operations.convolution as convolution
import operations.negative as negative

from operations.monochrome import GrayscaleMatrix


def prewitt():
    x_mask = ((1, 0, -1),
              (1, 0, -1),
              (1, 0, -1))

    y_mask = ((1, 1, 1),
              (0, 0, 0),
              (-1, -1, -1))

    return x_mask, y_mask


def sobel():
    x_mask = ((1, 0, -1),
              (2, 0, -2),
              (1, 0, -1))

    y_mask = ((-1, -2, -1),
              (0, 0, 0),
              (1, 2, 1))

    return x_mask, y_mask


def detect_borders_laplace():
    pass


def apply_border_detection(image, method=prewitt):
    x_mask, y_mask = method()
    matrix = GrayscaleMatrix.from_image(image)
    result = convolution.apply_all(matrix, x_mask, y_mask)
    result.apply_to(image)


if __name__ == '__main__':
    import imageio

    from argparse import ArgumentParser

    parser = ArgumentParser(description='Scale image')
    parser.add_argument('input_file', metavar='image', help='')
    parser.add_argument('-o', '--out', dest='output_file', nargs='?', help='')
    parser.add_argument('-m', '--method', dest='method', nargs='?', choices=['prewitt', 'sobel', 'laplace'], default='prewitt', help='')
    parser.add_argument('-n', '--negative', dest='negative', action='store_true')

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file or input_file

    methods = {'prewitt': prewitt, 'sobel': sobel}

    image = imageio.read(input_file)
    apply_border_detection(image, methods[args.method])

    if args.negative:
        negative.apply_negative(image)

    imageio.write(image, output_file)
