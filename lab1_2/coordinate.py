from __future__ import annotations
from enum import Enum


class Direction(Enum):
    LONGITUDE = 0
    LATITUDE = 1


class CoordinateDS():
    """ Abbreviations in this class:
        d - degree
        m - minute
        s - second
        D - direction
    """

    _CARDINAL_DIRECTIONS = (('N', 'S'), ('W', 'E'))

    def __init__(self, degrees: int = 0, minutes: int = 0, seconds: int = 0,
                 direction: Direction = Direction.LONGITUDE):
        self._degrees: int = 0
        self._minutes: int = 0
        self._seconds: int = 0

        self.direction = direction
        self.degrees = degrees
        self.minutes = minutes
        self.seconds = seconds

        self.abs_degrees = (abs(self.degrees) + self.minutes / 60 + self.seconds / 3600) * (-1 if self.degrees < 0 else 1)

    def get_format_ddmmssD(self):
        return (f'{abs(self.degrees)}° {self.minutes}\' {self.seconds}″'
                f' {self.cardinal_direction}')

    def get_format_ddddD(self):
        return f'{abs(self.abs_degrees)}° {self.cardinal_direction}'

    def get_coordinate_beetween_current_and(self, coord: CoordinateDS):
        if self.direction == coord.direction:
            coord1 = CoordinateDS()
            coord1.abs_degrees = (self.abs_degrees + coord.abs_degrees) / 2
            coord1.degrees, coord1.minutes, coord1.seconds = CoordinateDS.get_ddmmss(coord1.abs_degrees)
            return coord1.get_format_ddmmssD()
        else:
            return None

    @classmethod
    def get_ddmmss(cls, abs_degrees):
        degrees = int(abs_degrees)
        abs_minutes = abs(abs_degrees - degrees) * 60
        minutes = int(abs_minutes)
        seconds = int(abs_minutes - minutes)
        return degrees, minutes, seconds

    @classmethod
    def get_coordinate_beetween(cls, coord1: CoordinateDS,
                                coord2: CoordinateDS):
        if coord1.direction == coord2.direction:
            coord3 = CoordinateDS()
            coord3.abs_degrees = (coord1.abs_degrees + coord2.abs_degrees) / 2
            coord3.degrees, coord3.minutes, coord3.seconds = CoordinateDS.get_ddmmss(coord3.abs_degrees)
            return coord3.get_format_ddmmssD()
        else:
            return None

    @property
    def cardinal_direction(self):
        if self.degrees > 0:
            return self._CARDINAL_DIRECTIONS[self.direction.value][0]
        elif self.degrees < 0:
            return self._CARDINAL_DIRECTIONS[self.direction.value][1]
        else:
            return ' '

    @property
    def degrees(self) -> int:
        return self._degrees

    @degrees.setter
    def degrees(self, value) -> None:
        if (
            (
                self.direction is Direction.LONGITUDE
                and value >= -180 and value <= 180
            )
            or
            (
                self.direction is Direction.LATITUDE
                and value >= -90 and value <= 90
            )
        ):
            self._degrees = value
        else:
            raise ValueError(f'Degrees value <{value}> is incorrect')

    @property
    def minutes(self) -> int:
        return self._minutes

    @minutes.setter
    def minutes(self, value) -> None:
        if value >= 0 and value <= 59:
            self._minutes = value
        else:
            raise ValueError(f'Minutes value <{value}> is incorrect')

    @property
    def seconds(self) -> int:
        return self._seconds

    @seconds.setter
    def seconds(self, value) -> None:
        if value >= 0 and value <= 59:
            self._seconds = value
        else:
            raise ValueError(f'Seconds value <{value}> is incorrect')

    def __str__(self):
        return (f'<Coordinate: degrees - {self.degrees};'
                f' minutes - {self.minutes};'
                f' seconds - {self.seconds};'
                f' direction - {self.direction};'
                f' cardinal_direction - {self.cardinal_direction}>')
