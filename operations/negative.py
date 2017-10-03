#!/usr/bin/env python3
# negative.py


def apply_negative(image):
    for x, y in image:
        image.reds[x][y] = 255 - image.reds[x][y]
        image.greens[x][y] = 255 - image.greens[x][y]
        image.blues[x][y] = 255 - image.blues[x][y]


if __name__ == '__main__':
    import sys
    import imageio

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else input_file

    image = imageio.read(input_file)
    apply_negative(image)
    imageio.write(image, output_file)
