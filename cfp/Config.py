from InputData import InputData
import numpy as np


class Config:
    def __init__(self, list_machines, list_parts, input_data: InputData):
        self.input_data = input_data

        self.list_machines = list_machines
        self.list_parts = list_parts

        self.list_id_clusters = self.get_id_clusters()
        self.amount_clusters = len(self.list_id_clusters)

        self.dict_cluster_parts = self.get_dict_cluster_parts()
        self.dict_cluster_machines = self.get_dict_cluster_machines()

        self.amount_ones = input_data.amount_ones
        self.amount_ones_in = 0
        self.amount_zeros_in = 0
        self.calculate_ones_zeros()

        self.grouping_efficacy = Config.calculate_ge(self.amount_ones, self.amount_ones_in, self.amount_zeros_in)

    def __str__(self):
        return f"List machines: {' '.join(list(map(str, self.list_machines)))}\n" \
               f"List parts: {' '.join(list(map(str, self.list_parts)))}\n" \
               f"GE: {self.grouping_efficacy}"

    def get_id_clusters(self):
        return list(set(self.list_machines))

    def get_dict_cluster_parts(self):
        result_dict = {}
        for id_cluster in self.list_id_clusters:
            result_dict[id_cluster] = [ind for ind, cluster in enumerate(self.list_parts) if cluster == id_cluster]

        return result_dict

    def get_dict_cluster_machines(self):
        result_dict = {}
        for id_cluster in self.list_id_clusters:
            result_dict[id_cluster] = [ind for ind, cluster in enumerate(self.list_machines) if cluster == id_cluster]

        return result_dict

    def calculate_ones_zeros(self):
        amount_ones_in = 0
        amount_zeros_in = 0
        for i, machine_cluster in enumerate(self.list_machines):
            for j, part_cluster in enumerate(self.list_parts):
                if part_cluster == machine_cluster:
                    if self.input_data.matrix[i][j]:
                        amount_ones_in += 1
                    else:
                        amount_zeros_in += 1

        self.amount_ones_in = amount_ones_in
        self.amount_zeros_in = amount_zeros_in

    @classmethod
    def calculate_ge(cls, amount_ones, amount_ones_in, amount_zeros_in):
        return amount_ones_in / (amount_ones + amount_zeros_in)


def generate_configs(min_cluster: int, max_cluster: int, number_configs: int, input_data: InputData):
    # генерим id кластеров
    list_id_cluster = [[id_cluster for id_cluster in range(1, k + 1)] for k in range(min_cluster, max_cluster + 1)]

    configs = []
    for i in range(number_configs):
        # рандомно выбираем количество кластеров в конфигурации
        number_clusters = np.random.randint(low=0, high=max_cluster - min_cluster + 1)

        # рандомно заполняем списки машин и деталей номерами кластеров (придумываем "новое" решение)
        list_machines = []
        list_parts = []

        list_machines.extend(list_id_cluster[number_clusters])
        list_parts.extend(list_id_cluster[number_clusters])

        list_machines.extend(np.random.choice(list_id_cluster[number_clusters],
                                              size=input_data.amount_machines - len(list_id_cluster[number_clusters])))
        list_parts.extend(np.random.choice(list_id_cluster[number_clusters],
                                           size=input_data.amount_parts - len(list_id_cluster[number_clusters])))

        list_machines = list(map(int, np.random.permutation(list_machines)))
        list_parts = list(map(int, np.random.permutation(list_parts)))

        configs.append(Config(list_machines, list_parts, input_data))

    return configs


if __name__ == '__main__':
    pass
