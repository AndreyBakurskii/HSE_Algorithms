from math import sqrt


class Point:
    def __init__(self, id: int, x: float, y: float):
        self._id = id
        self._x = x
        self._y = y

    def __str__(self):
        return f"{self._id}: {self._x} {self._y}"

    def get_id(self):
        return self._id

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y


class Distance:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2
        self.dist = Distance.distance(point1, point2)

    @classmethod
    def distance(cls, point1: Point, point2: Point) -> float:
        return sqrt((point1.get_x() - point2.get_x()) ** 2 + (point1.get_y() - point2.get_y()) ** 2)

    @classmethod
    def distance_path(cls, path: list):
        res = 0
        for i in range(1, len(path)):
            res += Distance.distance(path[i - 1], path[i])

        return res


if __name__ == '__main__':
    pass
