import numpy as np

from Point import Point, Distance
from Solution import Solution


def greedy(matrix_distance: list, start=0, initial=False, return_path=False) -> Solution or list:

    path = []
    path_id = set()
    i = start
    while len(path) != len(matrix_distance):
        # добавляем вершину в результирующий путь
        path.append(matrix_distance[i][i].point1)
        path_id.add(matrix_distance[i][i].point1.get_id())

        # находим минимальную стоимость
        future_point_index = -1
        min_dist = float("inf")
        for ind, dist in enumerate(matrix_distance[i]):
            if dist.dist < min_dist and dist.point2.get_id() not in path_id:
                min_dist = dist.dist
                future_point_index = ind

        i = future_point_index

    if initial:
        path.append(matrix_distance[start][start].point1)

    if return_path:
        return path

    return Solution(path)


def local(initial_solution: Solution):
    """
    local search by 2-opt
    :param initial_solution:
    :return:
    """
    # print("Start 2-opt")
    length_path = initial_solution.get_length()

    best_solution = initial_solution
    best_path = initial_solution.get_path().copy()

    it_improved = True

    while it_improved:
        it_improved = False

        for i in range(1, length_path - 2):
            for j in range(i + 2, length_path):
                prev = Distance.distance(best_path[i - 1], best_path[i]) + Distance.distance(best_path[j - 1],
                                                                                             best_path[j])
                fut = Distance.distance(best_path[j], best_path[i]) + Distance.distance(best_path[j - 1],
                                                                                        best_path[i - 1])

                if prev > fut:
                    best_path[i:j] = best_path[j - 1:i - 1: -1]
                    best_solution = Solution(best_path)
                    it_improved = True

    return best_solution


def perturbation(solution: Solution, history: list):
    """
    perturbation by 3-opt with random selection of segment vertices
    :param solution:
    :param history:
    :return:
    """
    length = solution.get_length()

    best_solution = None
    best_path = []

    for iteration in range(10 ** 4):
        i = np.random.randint(low=1, high=length - 4)
        j = np.random.randint(low=i + 2, high=length - 2)
        k = np.random.randint(low=j + 2, high=length)

        comb1 = best_path[:i] + best_path[i:j - 1 + 1] + best_path[j:k - 1 + 1] + best_path[k:]
        comb2 = best_path[:i] + best_path[i:j - 1 + 1] + best_path[j:k - 1 + 1][::-1] + best_path[k:]
        comb3 = best_path[:i] + best_path[i:j - 1 + 1][::-1] + best_path[j:k - 1 + 1] + best_path[k:]
        comb4 = best_path[:i] + best_path[i:j - 1 + 1][::-1] + best_path[j:k - 1 + 1][::-1] + best_path[k:]
        comb5 = best_path[:i] + best_path[j:k - 1 + 1] + best_path[i:j - 1 + 1] + best_path[k:]
        comb6 = best_path[:i] + best_path[j:k - 1 + 1] + best_path[j - 1:i - 1:-1] + best_path[k:]
        comb7 = best_path[:i] + best_path[k - 1:j - 1:-1] + best_path[i:j - 1 + 1] + best_path[k:]
        comb8 = best_path[:i] + best_path[k - 1:j - 1:-1] + best_path[j - 1:i - 1: -1] + best_path[k:]

        combinations = [comb1, comb2, comb3, comb5, comb7, comb4, comb6, comb8]

        combinations = sorted(combinations, key=lambda comb: Distance.distance_path(comb))
        new_solution = Solution(combinations[0])

        if i == 0:
            best_solution = new_solution
            best_path = new_solution.get_path().copy()
            continue

        if new_solution.get_cost() < best_solution.get_cost():
            best_solution = new_solution
            best_path = new_solution.get_path().copy()

    return best_solution


def acceptance_criterion(new_solution_cost: tuple, history_cost: list):
    if history_cost.count(new_solution_cost) >= 4:
        return False
    return True


def iterated_local_search(initial_solution: Solution, amount_iter):
    cost_history = []
    solution = local(initial_solution)

    best_solution = solution
    best_solution_cost = best_solution.get_cost()

    i = amount_iter
    while i != 0:
        new_solution = local(perturbation(solution, cost_history))
        new_solution_cost = new_solution.get_cost()
        cost_history.append((new_solution_cost, new_solution.get_str_path()))

        if best_solution_cost > new_solution_cost:
            best_solution = new_solution

        if not acceptance_criterion(new_solution_cost, cost_history):
            return best_solution

        i -= 1

    return best_solution
