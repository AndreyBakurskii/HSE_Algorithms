from input_data import read_data
from Point import *
from algorithms import *


files = ["./data/instances/mona_1000.txt", "./data/instances/lu980.txt", "./data/instances/ja_1000.txt", "./data/instances/random_1.txt", "./data/instances/random_2.txt", "./data/instances/random_3.txt"]
for file in files:
    data = read_data(file)
    matrix_distance = [[Distance(point1, point2) for point2 in data] for point1 in data]

    solution = iterated_local_search(greedy(matrix_distance), amount_iter=20)

    cost = solution.get_cost() + Distance.distance(solution.get_path()[-1], solution.get_path()[0])
    print(f"{file}: {solution}")
    print(f"{file}: {cost}")
