def correct_gamma(image, gamma=1):
    for x, y in image:
        red = image.get_red(x, y, float)
        green = image.get_green(x, y, float)
        blue = image.get_blue(x, y, float)

        image.set_red(x, y, red ** (1 / gamma))
        image.set_green(x, y, green ** (1 / gamma))
        image.set_blue(x, y, blue ** (1 / gamma))

        image.reds[x][y] = image.reds[x][y] ** (1 / gamma)
