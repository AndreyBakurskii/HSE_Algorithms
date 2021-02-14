from Config import Config
import numpy as np


def initial_config(configs: list) -> Config:
    best = configs[0]

    for ind, config in enumerate(configs):
        solution = improve_config(config)
        if solution.grouping_efficacy > best.grouping_efficacy:
            best = solution
    return best


def improve_config(initial_config: Config) -> Config:

    config = initial_config

    improved = True
    while improved:

        improved = False

        best_delta_part = 0
        change_part_index = -1
        change_part_to_cluster = -1
        for index, from_cluster in enumerate(config.list_parts):
            if len(config.dict_cluster_parts[from_cluster]) == 1:
                continue

            for to_cluster in config.list_id_clusters:
                if from_cluster == to_cluster:
                    continue

                current_ge = get_ge_after_change_part(index_part=index,
                                                      from_cluster=from_cluster,
                                                      to_cluster=to_cluster,
                                                      config=config)

                current_delta = current_ge - config.grouping_efficacy

                if current_delta > best_delta_part:
                    best_delta_part = current_delta

                    change_part_index = index
                    change_part_to_cluster = to_cluster

                    improved = True

        best_delta_machine = 0
        change_machine_index = -1
        change_machine_to_cluster = -1
        for index, from_cluster in enumerate(config.list_machines):
            if len(config.dict_cluster_machines[from_cluster]) == 1:
                continue
            for to_cluster in config.list_id_clusters:
                if from_cluster == to_cluster:
                    continue

                current_ge = get_ge_after_change_machine(index_machine=index,
                                                         from_cluster=from_cluster,
                                                         to_cluster=to_cluster,
                                                         config=config
                                                         )
                current_delta = current_ge - config.grouping_efficacy

                if current_delta > best_delta_machine:
                    best_delta_machine = current_delta

                    change_machine_index = index
                    change_machine_to_cluster = to_cluster

                    improved = True

        if best_delta_part == 0 and best_delta_machine == 0:
            break

        elif best_delta_part > best_delta_machine:
            list_parts_copied = config.list_parts.copy()
            list_parts_copied[change_part_index] = change_part_to_cluster
            config = Config(config.list_machines, list_parts_copied, config.input_data)

        else:
            list_machines_copied = config.list_machines.copy()
            list_machines_copied[change_machine_index] = change_machine_to_cluster
            config = Config(list_machines_copied, config.list_parts, config.input_data)

    return config


def get_ge_after_change_part(index_part, from_cluster, to_cluster, config):
    zeros_from = 0
    ones_from = 0

    zeros_to = 0
    ones_to = 0

    for index_machine in config.dict_cluster_machines[from_cluster]:
        if config.input_data.matrix[index_machine][index_part]:
            ones_from += 1
        else:
            zeros_from += 1

    for index_machine in config.dict_cluster_machines[to_cluster]:
        if config.input_data.matrix[index_machine][index_part]:
            ones_to += 1
        else:
            zeros_to += 1

    return Config.calculate_ge(config.amount_ones,
                               config.amount_ones_in - ones_from + ones_to,
                               config.amount_zeros_in - zeros_from + zeros_to)


def get_ge_after_change_machine(index_machine, from_cluster, to_cluster, config):
    zeros_from = 0
    ones_from = 0

    zeros_to = 0
    ones_to = 0

    for index_part in config.dict_cluster_parts[from_cluster]:
        if config.input_data.matrix[index_machine][index_part]:
            ones_from += 1
        else:
            zeros_from += 1

    for index_part in config.dict_cluster_parts[to_cluster]:
        if config.input_data.matrix[index_machine][index_part]:
            ones_to += 1
        else:
            zeros_to += 1

    return Config.calculate_ge(config.amount_ones,
                               config.amount_ones_in - ones_from + ones_to,
                               config.amount_zeros_in - zeros_from + zeros_to)


def merge_clusters(config: Config):
    while True:
        from_cluster, to_cluster = list(map(int, np.random.choice(config.list_id_clusters, size=2)))
        if from_cluster == to_cluster:
            continue

        new_list_machines = [to_cluster if cluster == from_cluster else cluster for cluster in config.list_machines]
        new_list_parts = [to_cluster if cluster == from_cluster else cluster for cluster in config.list_parts]

        return Config(new_list_machines, new_list_parts, config.input_data)


def split_clusters(config: Config):
    while True:
        from_cluster = int(np.random.choice(config.list_id_clusters, size=1)[0])
        if len(config.dict_cluster_parts[from_cluster]) == 1 or len(config.dict_cluster_machines[from_cluster]) == 1:
            continue

        to_cluster = config.amount_clusters + 1
        index_machine = int(np.random.choice(config.dict_cluster_machines[from_cluster], size=1)[0])
        index_parts = int(np.random.choice(config.dict_cluster_parts[from_cluster], size=1)[0])

        new_list_machines = config.list_machines.copy()
        new_list_machines[index_machine] = to_cluster

        new_list_parts = config.list_parts.copy()
        new_list_parts[index_parts] = to_cluster

        return Config(new_list_machines, new_list_parts, config.input_data)


def general_vns(config: Config, k: int):
    l = 1
    go_split = True
    go_merge = False
    max_clusters = min(config.input_data.amount_parts, config.input_data.amount_machines)
    min_clusters = 2
    if config.amount_clusters == max_clusters:
        go_merge = True
        go_split = False

    while l < k:
        configs = []
        if go_split:
            configs = [split_clusters(config) for _ in range(30)]

        else:
            configs = [split_clusters(config) for _ in range(10)]

        best_new_config = None
        best_ge = 0
        for new_config in configs:
            new_config = improve_config(new_config)
            if new_config.grouping_efficacy > best_ge:
                best_new_config = new_config
                best_ge = best_new_config.grouping_efficacy

        if best_new_config.grouping_efficacy > config.grouping_efficacy:
            l = 1
            config = best_new_config
            if go_split:
                if config.amount_clusters == max_clusters:
                    go_split = False
                    go_merge = True

            else:
                if config.amount_clusters == min_clusters:
                    go_split = True
                    go_merge = False
        else:
            l += 1
            if go_split:
                if config.amount_clusters != min_clusters:
                    go_split = False
                    go_merge = True

            else:
                if config.amount_clusters != max_clusters:
                    go_split = True
                    go_merge = False

    return config
