from InputData import InputData
from algorithms import initial_config, general_vns
from Config import Config, generate_configs
import time

print(time.ctime())

path = "./data/cfp/king30x90.txt"
input_data = InputData(path)

start_configs = generate_configs(2, min(input_data.amount_machines, input_data.amount_parts), 40, input_data)
optimal_config = initial_config(start_configs)

config = general_vns(optimal_config, 15)

print("Best config:")
print(config)

print(time.ctime())
