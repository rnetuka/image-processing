class LabColor:

    def __init__(self, l, a, b):
        self.l = l
        self.a = a
        self.b = b

    @property
    def lightness(self):
        return self.l

    @staticmethod
    def from_rgb(r, g, b):
        r = r / 255
        g = g / 255
        b = b / 255

        r = pow((r + 0.055) / 1.055, 2.4) if r > 0.04045 else r / 12.92
        g = pow((g + 0.055) / 1.055, 2.4) if g > 0.04045 else g / 12.92
        b = pow((b + 0.055) / 1.055, 2.4) if b > 0.04045 else b / 12.92

        r *= 100
        g *= 100
        b *= 100

        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505

        x = x / 95.047
        y = y / 100.0
        z = z / 108.883

        x = pow(x, 1 / 3) if x > 0.008856 else 7.787 * x + 16 / 116
        y = pow(y, 1 / 3) if y > 0.008856 else 7.787 * y + 16 / 116
        z = pow(z, 1 / 3) if z > 0.008856 else 7.787 * z + 16 / 116

        l = 116 * y - 16
        a = 500 * (x - y)
        b = 200 * (y - z)

        return LabColor(l, a, b)

    def to_rgb(self):
        from color.rgb import RgbColor
        return RgbColor.from_lab(self.l, self.a, self.b)

    def __str__(self):
        return 'Lab({}, {}, {})'.format(self.l, self.a, self.b)

    @staticmethod
    def from_string(string):
        i = string.find('(')
        j = string.find(')')

        color_model = string[:i]

        if i < 0 or j < 0 or color_model.lower() != 'lab':
            raise ValueError('Cannot parse LAB color from "{}"'.format(string))

        values = string[(i + 1):j]
        values = values.split(',')
        values = [int(n) for n in values]
        return LabColor(*values)
