from Point import Point

PATH2DATA = "./test_data.txt"


def read_data(path2file: str) -> list:
    list_points = []

    with open(path2file, "r") as file_data:
        n = list(map(int, file_data.readline().strip().split()))[0]

        for i in range(n):
            id_vertex, x, y = list(map(float, file_data.readline().strip().split()))
            list_points.append(Point(int(id_vertex), x, y))

    return list_points


if __name__ == '__main__':
    data = read_data(PATH2DATA)
    for point in data:
        print(point)
