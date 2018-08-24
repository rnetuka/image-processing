class RgbColor:

    def __init__(self, r, g, b):
        if all(type(component) is int for component in [r, g, b]):
            if any(255 < component < 0 for component in [r, g, b]):
                raise ValueError('RGB components must be between 0 and 255')

        if all(type(component) is float for component in [r, g, b]):
            if any(1.0 < component < 0.0 for component in [r, g, b]):
                raise ValueError('RGB components must be between 0.0 and 1.0')

            r = int(r * 255)
            g = int(g * 255)
            b = int(b * 255)

        self.r = r
        self.g = g
        self.b = b

    @property
    def red(self):
        return self.r

    @property
    def green(self):
        return self.g

    @property
    def blue(self):
        return self.b

    def to_lab(self):
        from color.lab import LabColor
        return LabColor.from_rgb(self.r, self.g, self.b)

    def __repr__(self):
        return 'rgb({}, {}, {})'.format(self.r, self.g, self.b)

    @staticmethod
    def from_string(string):
        i = string.find('(')
        j = string.find(')')

        color_model = string[:i]

        if i < 0 or j < 0 or color_model.lower() != 'rgb':
            raise ValueError('Cannot parse RGB color from "{}"'.format(string))

        values = string[(i + 1):j]
        values = values.split(',')
        values = [int(n) for n in values]
        return RgbColor(*values)

    @staticmethod
    def from_lab(l, a, b):
        y = (l + 16) / 116.0
        x = a / 500.0 + y
        z = y - b / 200.0

        x = pow(x, 3) if pow(x, 3) > 0.008856 else (x - 16.0 / 116) / 7.787
        y = pow(y, 3) if pow(y, 3) > 0.008856 else (y - 16.0 / 116) / 7.787
        z = pow(z, 3) if pow(z, 3) > 0.008856 else (z - 16.0 / 116) / 7.787

        x *= 95.047
        y *= 100
        z *= 108.883

        x = x / 100
        y = y / 100
        z = z / 100

        r = x * 3.2406 + y * -1.5372 + z * -0.4986
        g = x * -0.9689 + y * 1.8758 + z * 0.0415
        b = x * 0.0557 + y * -0.2040 + z * 1.0570

        r = 1.055 * pow(r, 1 / 2.4) - 0.055 if r > 0.0031308 else 12.92 * r
        g = 1.055 * pow(g, 1 / 2.4) - 0.055 if g > 0.0031308 else 12.92 * g
        b = 1.055 * pow(b, 1 / 2.4) - 0.055 if b > 0.0031308 else 12.92 * b

        r = max(0.0, min(r, 1.0))
        g = max(0.0, min(g, 1.0))
        b = max(0.0, min(b, 1.0))

        return RgbColor(r, g, b)


if __name__ == '__main__':
    import sys
    from color.lab import LabColor

    input_color = sys.argv[1]
    input_color = LabColor.from_string(input_color)

    print(input_color.to_rgb())
