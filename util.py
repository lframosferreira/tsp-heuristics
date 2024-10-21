import os
import time

import networkx
import pandas as pd
import tsplib95

from algorithms import christofides, twice_around_the_tree

NUMBER_OF_EXECUTIONS: int = 20
INSTANCES_FOLDER: str = "instances/tsplib95"

def get_graph_from_tsplib95_file(filepath: str, is_euc_2d: bool = True)->networkx.Graph:
    if is_euc_2d:
        return tsplib95.load(filepath).get_graph()
    else:
        problem = tsplib95.load(filepath)
        problem._wfunc = lambda start, end: tsplib95.distances.pseudo_euclidean(problem.node_coords[start], problem.node_coords[end])
        return problem.get_graph()

def get_time_for_every_instance_and_dump(filename: str = "output.csv") -> None:
    df: pd.DataFrame = pd.DataFrame(
        columns=["algorithm", "instance", "path_weight", "time"]
    )
    for file in os.listdir(INSTANCES_FOLDER):
        graph: networkx.Graph = get_graph_from_tsplib95_file(f"{INSTANCES_FOLDER}/{file}", not file.startswith("att"))
        total_time: float = 0.0
        weight: int = 0
        for _ in range(NUMBER_OF_EXECUTIONS):
            start: float = time.perf_counter()
            path = twice_around_the_tree(graph)
            weight = networkx.path_weight(graph, path, "weight")
            end: float = time.perf_counter()
            total_time += end - start
        df = pd.concat(
            [
                pd.DataFrame(
                    [["tatt", file, weight, total_time / NUMBER_OF_EXECUTIONS]],
                    columns=df.columns,
                ),
                df,
            ],
            ignore_index=True,
        )

    df.to_csv(filename)
