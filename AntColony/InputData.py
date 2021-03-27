from math import sqrt


def is_prime(number: int):
    if number % 2 == 0:
        return number == 2
    d = 3
    while d * d <= number and number % d != 0:
        d += 2
    return d * d > number


class InputData:
    def __init__(self, path2data, n):
        self.length = n
        self.path2data = path2data
        self.data = [0 for i in range(self.length)]
        self.distance_matrix = [[0 for i in range(self.length)] for j in range(self.length)]
        self.prime_cities = set([i for i in range(self.length) if is_prime(i)])

    def read_data(self):
        with open(self.path2data, 'r') as file:
            # пропуск первой строки
            file.readline()

            for i in range(self.length):
                id_ver, x, y = file.readline().strip().split(',')

                id_ver = int(id_ver)
                x, y = float(x), float(y)

                self.data[id_ver] = (x, y)

    def fill_distance_matrix(self):
        for i in range(self.length):
            for j in range(i, self.length):
                if i == j:
                    continue

                distance = self.calculate_distance(self.data[i][0], self.data[i][1], self.data[j][0], self.data[i][1])
                self.distance_matrix[i][j] = distance
                self.distance_matrix[j][i] = distance

    @staticmethod
    def calculate_distance(x_i, x_j, y_i, y_j):
        return sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)


if __name__ == '__main__':
    input_data = InputData('./data/cities.csv', 1000)
    input_data.read_data()
    input_data.fill_distance_matrix()

    print(input_data.prime_cities)

    # for ind, coord in enumerate(input_data.data):
    #     print(f"{ind} - {coord}")

    # for row in input_data.distance_matrix:
    #     print(*row)
