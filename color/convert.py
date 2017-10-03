import sys

from color.lab import LabColor
from color.rgb import RgbColor

# convert.py rgb(145, 217, 3) lab
if __name__ == '__main__':
    input_color = sys.argv[1]
    input_model = input_color[: input_color.find('(')]

    output_model = sys.argv[2]
    output_color = None

    if input_model == 'rgb':
        input_color = RgbColor.from_string(input_color)
    elif input_model == 'lab':
        input_color = LabColor.from_string(input_color)
    else:
        raise ValueError('Unknown color model: {}'.format(input_model))

    if output_model == 'lab':
        output_color = input_color.to_lab()
    elif output_model == 'rgb':
        output_color = input_color.to_rgb()
    else:
        raise ValueError('Unknown color model: {}'.format(output_model))

    print(output_color)
