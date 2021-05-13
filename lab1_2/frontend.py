from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

TEXT_OF_CODE = """
coord1 = CoordinateDS(12, 30, 40, Direction.LONGITUDE)
coord2 = CoordinateDS(-6, 30, 40, Direction.LONGITUDE)
print(coord2.get_format_ddmmssD())
print(coord2.get_format_ddddD())
print(coord2.get_coordinate_beetween_current_and(coord1))
print(CoordinateDS.get_coordinate_beetween(coord1, coord2))
"""

Builder.load_file('frontend.kv')


class Frontend(BoxLayout):
    pass
