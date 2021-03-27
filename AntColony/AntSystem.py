import numpy as np
import time
from InputData import InputData


class Path:
    def __init__(self, max_length, input_data: InputData):
        self.max_length = max_length
        self.cur_length = 0
        self.path = []
        self.edges = set()
        self.distance = 0

        self.input_data = input_data

    def __str__(self):
        if self.distance == 0:
            self.calculate_distance()

        return f"{self.path}\n" \
               f"{self.distance}"

    def append(self, new_city, head=False, tail=False):
        if not tail:
            if new_city in self.path:
                raise ValueError("Такой город уже есть в пути")

            if self.cur_length + 1 > self.max_length:
                raise IndexError("Добавление города приведет к переполнению")

        if not head:
            self.edges.add((self.path[-1], new_city))

        self.path.append(new_city)
        self.cur_length += 1

    def calculate_distance(self):
        if self.cur_length < 2:
            raise ValueError("Невозможно сосчитать длину пути, мало городов")

        distance = 0
        for index_city in range(self.cur_length - 1):
            from_city = self.path[index_city]
            to_city = self.path[index_city + 1]

            dist = self.input_data.distance_matrix[from_city][to_city]

            # if (index_city + 1) % 10 == 0 and from_city not in input_data.prime_cities:
            #     dist *= 1.1

            distance += dist

        # добавляем расстояние от последнего города до стартового
        # from_city = self.path[-1]
        # to_city = self.path[0]
        #
        # dist = self.input_data.distance_matrix[from_city][to_city]
        #
        # if self.cur_length % 10 == 0 and not is_prime(from_city):
        #     dist *= 1.1
        #
        # distance += dist
        self.distance = distance

        return distance


# обратить внимание на вычисление дистанции пути, 10 город должен быть простым, внести в рассчет вероятности для муравья
# Каждый 10-й шаг (stepNumber% 10 == 0) на 10% длиннее, если он не исходит от простого CityId.
# для определения города использовать np.choice(a, p=probability(распределение для каждого элемента))
class AntSystem:
    def __init__(self, input_data: InputData, start_value_pheromone=1, alpha=1, beta=1, evaporation_rate=0.5, q=1):
        self.input_data = input_data

        self.pheromone_matrix = self.initial_pheromone_matrix(start_value_pheromone)

        self.alpha = alpha
        self.beta = beta
        self.ro = evaporation_rate
        self.q = q

    def run(self, amount_iteration, amount_ant) -> Path:
        best_path = None
        best_distance = float("+inf")

        for _ in range(amount_iteration):
            best_path_iteration = None
            best_distance_iteration = float("+inf")

            paths = []
            for i in range(amount_ant):
                path = self.run_ant()
                distance = path.calculate_distance()
                paths.append(path)

                # обновляем лучший путь среди одной итерации
                if best_distance_iteration > distance:
                    best_path_iteration = path
                    best_distance_iteration = distance

            # обновляем лучший путь среди всех итерации
            if best_distance > best_distance_iteration:
                best_path = best_path_iteration
                best_distance = best_distance_iteration

            print(best_path)
            print()
            self.update_pheromone_matrix(paths)

        return best_path

    def run_ant(self):
        list_available_cities = [i for i in range(1, self.input_data.length)]
        start_city = 0
        step_number = 1

        ant_path = Path(self.input_data.length, self.input_data)
        ant_path.append(start_city, head=True)

        from_city = start_city
        while len(list_available_cities) != 0:
            denominator = self._calc_pr_den(from_city, list_available_cities, step_number)

            probabilities = [self.calculate_probability(self._calc_pr_num(from_city, to_city, step_number), denominator)
                             for to_city in list_available_cities]

            to_city = int(np.random.choice(list_available_cities, p=probabilities))
            ant_path.append(to_city)

            list_available_cities.remove(to_city)

            from_city = to_city
            step_number += 1

        ant_path.append(ant_path.path[0], tail=True)

        return ant_path

    def calculate_probability(self, numerator, denominator):
        return numerator / denominator

    # calculate numerator of probability
    def _calc_pr_num(self, from_city, to_city, step_number):
        t = self.pheromone_matrix[from_city][to_city] ** self.alpha

        n = self.calculate_distance(from_city, to_city) ** self.beta
        # if step_number % 10 == 0 and from_city not in input_data.prime_cities:
        #     n *= (1.1 ** self.beta)

        return t * n

    # calculate denominator of probability
    def _calc_pr_den(self, from_city, list_cities, step_number):
        result = 0
        for to_city in list_cities:
            result += self._calc_pr_num(from_city, to_city, step_number)
        return result

    def update_pheromone_matrix(self, paths):
        self._evaporation()
        self._add_pheromone(paths)

    def _evaporation(self):
        for i in range(self.input_data.length):
            for j in range(self.input_data.length):
                if i == j:
                    continue
                self.pheromone_matrix[i][j] *= self.ro

    def _add_pheromone(self, paths):
        for path in paths:
            if path.distance == 0:
                path.calculate_distance()

            for edge in path.edges:
                self.pheromone_matrix[edge[0]][edge[1]] += (self.q / path.distance)
                # self.pheromone_matrix[edge[0]][edge[1]] += 0.5

    def calculate_distance(self, from_city, to_city):
        return self.input_data.distance_matrix[from_city][to_city]

    def initial_pheromone_matrix(self, start_value_pheromone):
        pheromone_matrix = [[start_value_pheromone if i != j else 0 for i in range(self.input_data.length)]
                            for j in range(self.input_data.length)]

        return pheromone_matrix


if __name__ == '__main__':

    input_data = InputData('./data/cities.csv', 100)
    input_data.read_data()
    input_data.fill_distance_matrix()

    ant_system = AntSystem(input_data=input_data, evaporation_rate=0.9)
    path = ant_system.run(amount_iteration=100, amount_ant=100)

    print(path)