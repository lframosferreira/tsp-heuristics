import networkx
import tsplib95
import os
import time
import pandas as pd
import numpy as np
from util import get_graph_from_tsplib95_file

NUMBER_OF_EXECUTIONS: int = 20
INSTANCES_FOLDER: str = "instances/tsplib95"


def two_opt(
    current_tour: list[int], current_cost: int, graph: np.array, i: int, j: int
) -> tuple[int, list[int]]:
    # swaping i and j indices in the tour
    new_tour: list[int] = (
        current_tour[:i] + current_tour[i : j + 1][::-1] + current_tour[j + 1 :]
    )
    # number of cities
    n: int = len(new_tour)
    new_cost: int = (
        current_cost
        - graph[current_tour[(i - 1) % n], current_tour[i]]
        - graph[current_tour[j], current_tour[(j + 1) % n]]
        + graph[current_tour[(i - 1) % n], current_tour[j]]
        + graph[current_tour[i], current_tour[(j + 1) % n]]
    )
    return new_cost, new_tour


# based on the pseudocode available at https://en.wikipedia.org/wiki/2-opt
def vnd(graph: np.array) -> tuple[int, list[int]]:
    number_of_nodes: int = graph.shape[0]
    current_tour: list[int] = list(range(number_of_nodes))
    current_tour_cost: int = 0
    for i in range(number_of_nodes):
        current_tour_cost += graph[i][(i + 1) % number_of_nodes]
    solution_has_improved = True
    while solution_has_improved:
        solution_has_improved = False
        for i in range(number_of_nodes):
            for j in range(i + 1, number_of_nodes):
                if j - i == number_of_nodes - 1:
                    continue
                new_tour_cost, new_tour = two_opt(
                    current_tour, current_tour_cost, graph, i, j
                )
                if new_tour_cost < current_tour_cost:
                    current_tour = new_tour
                    current_tour_cost = new_tour_cost
                    solution_has_improved = True
    return current_tour_cost, current_tour


def get_time_for_every_instance_and_dump(
    filename: str = "output_vnd.csv",
) -> None:
    df: pd.DataFrame = pd.DataFrame(
        columns=["algorithm", "instance", "path_weight", "time"]
    )
    for file in os.listdir(INSTANCES_FOLDER):
        nx_graph = get_graph_from_tsplib95_file(
            f"{INSTANCES_FOLDER}/{file}", not file.startswith("att")
        )
        graph = networkx.adjacency_matrix(nx_graph).toarray()
        cost, _ = vnd(graph)
        total_time: float = 0.0
        weight: int = 0
        for _ in range(NUMBER_OF_EXECUTIONS):
            start: float = time.perf_counter()
            weight = cost
            end: float = time.perf_counter()
            total_time += end - start
        df = pd.concat(
            [
                pd.DataFrame(
                    [["2-OPT", file, weight, total_time / NUMBER_OF_EXECUTIONS]],
                    columns=df.columns,
                ),
                df,
            ],
            ignore_index=True,
        )

    df.to_csv(filename)


get_time_for_every_instance_and_dump()
