from coordinate import CoordinateDS, Direction


def run_backend():
    coord1 = CoordinateDS(12, 30, 40, Direction.LONGITUDE)
    coord2 = CoordinateDS(-6, 30, 40, Direction.LONGITUDE)
    return '\n'.join((
        str(coord2.get_format_ddmmssD()),
        str(coord2.get_format_ddddD()),
        str(coord2.get_coordinate_beetween_current_and(coord1)),
        str(CoordinateDS.get_coordinate_beetween(coord1, coord2))
    ))
