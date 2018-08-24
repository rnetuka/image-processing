from image import Image


def nearest_neighbor(image, ratio):
    new_width = int(image.width * ratio)
    new_height = int(image.height * ratio)

    result = Image(new_width, new_height)

    for x, y in result.coordinates:
        i = int(x / ratio)
        j = int(y / ratio)

        di = x / ratio - i
        dj = y / ratio - j

        if i < 0 or j < 0 or i + 1 == image.width or j + 1 == image.height:
            color = image.get_argb(i, j)
        else:
            nearest_i = i if (1 - di) < di else i + 1
            nearest_j = j if (1 - dj) < dj else j + 1
            color = image.get_argb(nearest_i, nearest_j)

        result.set_rgb(x, y, color)

    return result


def bilinear_interpolation(image, ratio):
    new_width = int(image.width * ratio)
    new_height = int(image.height * ratio)

    result = Image(new_width, new_height)

    for x, y in result.coordinates:
        i = int(x / ratio)
        j = int(y / ratio)

        di = x / ratio - i
        dj = y / ratio - j

        if i < 0 or j < 0 or i + 1 == image.width or j + 1 == image.height:
            color = image.get_argb(i, j)
            red = (color >> 16) & 0xff
            green = (color >> 8) & 0xff
            blue = color & 0xff
        else:
            #
            # +---+---+
            # | a | b |
            # +---+---+
            # | c | d |
            # +---+---+
            #

            a_red = image.reds[i][j]
            a_green = image.greens[i][j]
            a_blue = image.blues[i][j]

            b_red = image.reds[i + 1][j]
            b_green = image.greens[i + 1][j]
            b_blue = image.blues[i + 1][j]

            c_red = image.reds[i][j + 1]
            c_green = image.greens[i][j + 1]
            c_blue = image.blues[i][j + 1]

            d_red = image.reds[i + 1][j + 1]
            d_green = image.greens[i + 1][j + 1]
            d_blue = image.blues[i + 1][j + 1]

            red = (b_red - a_red) * di + (c_red - a_red) * dj + (d_red + a_red - b_red - c_red) * di * dj + a_red
            green = (b_green - a_green) * di + (c_green - a_green) * dj + (d_green + a_green - b_green - c_green) * di * dj + a_green
            blue = (b_blue - a_blue) * di + (c_blue - a_blue) * dj + (d_blue + a_blue - b_blue - c_blue) * di * dj + a_blue

        result.set_red(x, y, int(red))
        result.set_green(x, y, int(green))
        result.set_blue(x, y, int(blue))

    return result


def scaled(image, ratio, method=bilinear_interpolation):
    return method(image, ratio)


# > scaling.py image.png -o scaled.png -r 0.5
# > scaling.py image.png -o scaled.png -r 0.5 -m nn
# > scaling.py image.png -o scaled.png --width 1080
# > scaling.py image.png -o scaled.png --height 560
if __name__ == '__main__':
    import imageio

    from argparse import ArgumentParser

    parser = ArgumentParser(description='Scale image')
    parser.add_argument('input_file', metavar='image', help='image to be scaled')
    parser.add_argument('-o', '--out', dest='output_file', nargs='?', help='output file (default: overwrite the input)')
    parser.add_argument('-m', '--method', dest='method', nargs='?', choices=['nn', 'bi'], default='bi', help='method for scaling (one of "nn" - nearest neighbour or "bi" - billinear interpolation (default))')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', '--ratio', dest='ratio', type=float, nargs='?', help='scale ratio')
    group.add_argument('--height', dest='height', type=int, nargs='?', help='new image height')
    group.add_argument('--width', dest='width', type=int, nargs='?', help='new image width')

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file or input_file

    image = imageio.read(input_file)

    if args.ratio:
        ratio = args.ratio
    elif args.width:
        ratio = args.width / image.width
    elif args.height:
        ratio = args.height / image.height

    methods = {'nn': nearest_neighbor, 'bi': bilinear_interpolation}

    image = scaled(image, ratio, methods[args.method])
    imageio.write(image, output_file)
