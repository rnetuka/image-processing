import sys

import imageio
from operations.grayscale import convert_to_grayscale
from operations.gamma import correct_gamma
from operations.negative import apply_negative

# main.py --negative --grayscale --gamma=0.3 -i venice.jpg -o venice2.jpg
if __name__ == '__main__':
    if '-i' in sys.argv:
        input_file = sys.argv[sys.argv.index('-i') + 1]
    else:
        input_file = sys.argv[1]

    if '-o' in sys.argv:
        output_file = sys.argv[sys.argv.index('-o') + 1]
    else:
        output_file = input_file

    print('Start...')

    image = imageio.read(input_file)

    print('Image read')

    if '--negative' in sys.argv:
        apply_negative(image)

    if '--grayscale' in sys.argv or '--greyscale' in sys.argv:
        convert_to_grayscale(image)

    if '--histogram' in sys.argv:
        import operations.histogram as histogram
        histogram.equalize(image)

    for argument in sys.argv:
        if argument.startswith('--gamma'):
            value = float(argument.split('='))
            correct_gamma(image, value)

    imageio.write(image, output_file)
    print('Output saved: {}'.format(output_file))