import networkx
import tsplib95
import os
import time
import pandas as pd
from util import get_graph_from_tsplib95_file

NUMBER_OF_EXECUTIONS: int = 20
INSTANCES_FOLDER: str = "instances/tsplib95"


def two_opt() -> tuple[int, list[int]]:
    return 0, []


def vnd(graph) -> list[int]:
    number_of_nodes: int = graph.shape[0]
    current_tour: list[int] = list(range(number_of_nodes))
    current_tour_cost: int = 0
    for i in range(number_of_nodes):
        current_tour_cost += graph[i][i + 1]
    solution_has_improved = True
    while solution_has_improved:
        solution_has_improved = False
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                new_tour_cost, new_tour = two_opt(current_tour, graph, i, j)
                continue
    return []


def get_time_for_every_instance_and_dump(
    filename: str = "output_metaheuristic.csv",
) -> None:
    df: pd.DataFrame = pd.DataFrame(
        columns=["algorithm", "instance", "path_weight", "time"]
    )
    for file in os.listdir(INSTANCES_FOLDER):
        nx_graph = get_graph_from_tsplib95_file(
            f"{INSTANCES_FOLDER}/{file}", not file.startswith("att")
        )
        graph = networkx.adjacency_matrix(nx_graph).toarray()
        path = vnd(graph)
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
