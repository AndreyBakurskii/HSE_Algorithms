from Point import Point, Distance


class Solution:
    def __init__(self, list_points: [Point]):
        self._path = list_points
        self._length = len(list_points)
        self._str_path = " ".join([str(point.get_id()) for point in self._path])
        self._cost = self.costing()

    def __str__(self):
        return self._str_path

    def costing(self):
        cost = 0
        for i in range(1, self._length):
            cost += Distance.distance(self._path[i - 1], self._path[i])

        return cost

    def get_cost(self):
        return self._cost

    def get_path(self):
        return self._path

    def get_length(self):
        return self._length

    def get_str_path(self):
        return self._str_path


if __name__ == '__main__':
    test_solution = Solution([Point(0, 0, 0), Point(1, 2, 0)])
    print(test_solution.get_cost())
    print(test_solution)
