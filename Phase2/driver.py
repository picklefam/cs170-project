from parse import *
from solver import solve
import networkx as nx
import os

if __name__ == "__main__":
    output_dir = "submission"
    input_dir = "inputs"
    count = 1
    for input_path in os.listdir(input_dir):
        graph_name = input_path.split(".")[0]
        print()
        print(count, f"{graph_name}")
        G = read_input_file(f"{input_dir}/{input_path}")
        T = solve(G)
        write_output_file(T, f"{output_dir}/{graph_name}.out")
        count += 1
