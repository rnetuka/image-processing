import operations.negative as negative
from color.grayscale import GrayscaleMatrix
from operations.convolution import ConvolutionMask
from operations.convolution import convolve


def normalize(value, lowerBound, upperBound):
    return (value - lowerBound) / (upperBound - lowerBound)


def apply(matrix, mask):
    result = GrayscaleMatrix(matrix.width, matrix.height, value_type=float)
    partial_result = convolve(matrix, mask)

    for x, y in result:
        result[x][y] = partial_result[x][y]

    lowest, highest = result.edge_values()

    for x, y in result:
        result[x][y] = normalize(result[x][y], lowest, highest)

    return result


def apply_all(matrix, *masks):
    result = GrayscaleMatrix(matrix.width, matrix.height, value_type=float)

    for mask in masks:
        partial_result = convolve(matrix, mask)

        for x, y in result:
            result[x][y] = abs(result[x][y]) + abs(partial_result[x][y])

    lowest, highest = result.edge_values()

    for x, y in result:
        result[x][y] = normalize(result[x][y], lowest, highest)

    return result


def apply_border_detection(image, method='prewitt'):
    matrix = GrayscaleMatrix.from_image(image, value_type=float)

    if method == 'prewitt':
        x_mask = ConvolutionMask((1, 1, 1), (0, 0, 0), (-1, -1, -1))
        y_mask = ConvolutionMask((-1, 0, 1), (-1, 0, 1), (-1, 0, 1))

        result = apply_all(matrix, x_mask, y_mask)

    elif method == 'sobel':
        x_mask = ConvolutionMask((1, 2, 1), (0, 0, 0), (-1, -2, -1))
        y_mask = ConvolutionMask((-1, 0, 1), (-2, 0, 2), (-1, 0, 1))

        result = apply_all(matrix, x_mask, y_mask)

    elif method == 'laplace':
        mask = ConvolutionMask((0, -1, 0), (-1, 4, -1), (0, -1, 0))
        result = apply(matrix, mask)

    elif method == 'laplace2':
        mask = ConvolutionMask((0, 1, 0), (1, -4, 1), (0, 1, 0))
        result = apply(matrix, mask)

    else:
        raise ValueError()

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

    image = imageio.read(input_file)
    apply_border_detection(image, args.method)

    if args.negative:
        negative.apply_negative(image)

    imageio.write(image, output_file)
