import os
import time

import networkx
import pandas as pd
import tsplib95

from algorithms import christofides, twice_around_the_tree

EUC_2D_DIR: str = "instances/EUC_2D"


def get_time_for_every_instance_and_dump(
    algorithm: str, filename: str = "output.csv"
) -> None:
    df: pd.DataFrame = pd.DataFrame(columns=["instance", "path_weight", "time"])
    for file in os.listdir(EUC_2D_DIR):
        graph = tsplib95.load(f"{EUC_2D_DIR}/{file}").get_graph()
        start: float = time.perf_counter()
        weight: int = 0
        if algorithm == "twice_around_the_tree":
            path = twice_around_the_tree(graph)
            weight = networkx.path_weight(graph, path, "weight")
        elif algorithm == "christofides":
            path = christofides(graph)
            weight = networkx.path_weight(graph, path, "weight")
        end: float = time.perf_counter()
        df = pd.concat(
            [pd.DataFrame([[file, weight, end - start]], columns=df.columns), df],
            ignore_index=True,
        )
    df.to_csv(filename)
