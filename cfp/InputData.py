class InputData:
    def __init__(self, path):
        with open(path, "r") as file:
            self.amount_machines, self.amount_parts = list(map(int, file.readline().split()))
            self.sparse_matrix = []
            for i in range(self.amount_machines):
                self.sparse_matrix.append(list(map(int, file.readline().split()))[1:])

        self.matrix = self.to_matrix()
        self.amount_ones = self.calculate_ones()

    def to_matrix(self):
        matrix = [[0 for _ in range(self.amount_parts)] for _ in range(self.amount_machines)]
        for i, column in enumerate(self.sparse_matrix):
            for j in column:
                matrix[i][j - 1] = 1

        return matrix

    def calculate_ones(self):
        amount_ones = 0
        for row in self.matrix:
            amount_ones += sum(row)

        return amount_ones


if __name__ == '__main__':
    # path = "./data/test_data_1.txt"
    # path = "./data/test_data_2.txt"
    path = "./data/test_data_3.txt"
    input_data = InputData(path)

    print(input_data.amount_machines, input_data.amount_parts)
    print(*input_data.sparse_matrix)

    for row in input_data.matrix:
        print(*row)
