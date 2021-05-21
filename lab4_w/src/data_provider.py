from math import pi, sin


def calculate_points(width, height):
    """
    Повертає кортеж координат графіка

    wight - ширина координатної площини
    height - висота координатної площини
    """

    x_start = -2 * pi
    x_end = 2 * pi
    w_correction = width / 2
    h_correction = height / 2
    # Масштаб віддображення графіка, чим більше значення, тим ближче графік
    scale = width / (x_end - x_start) - 10
    accuracy = 10  # Точність (кількість точок)
    points = [-2 * pi * scale + w_correction, h_correction]
    for t in range(int(x_start) * accuracy, int(x_end) * accuracy):
        x = t / accuracy
        abstract_x = x * scale + w_correction
        y = sin(x)
        abstract_y = y * scale + h_correction

        points.extend((abstract_x, abstract_y))
    points.extend((2 * pi * scale + w_correction, h_correction))
    return tuple(points)


def calculate_size(width, height, separator=2):
    size = int((width if width < height else height) / separator)
    return (size, size)


def calculate_pos(width, height, separator=2):
    size = calculate_size(width, height, separator)[0]
    return (int((width - size) / 2), int((height - size) / 2))


def calc_angle():
    rates = (80, 10, 5, 5)
    if sum(rates) != 100:
        return None
    else:
        angles = [0]
        for rate in rates:
            angles.append(360 * rate / 100 + angles[-1])
    return angles
