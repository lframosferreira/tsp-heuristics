import os
import time

import networkx
import pandas as pd
import tsplib95

from algorithms import christofides, twice_around_the_tree

EUC_2D_DIR: str = "instances/EUC_2D"
NUMBER_OF_EXECUTIONS: int = 20


def get_time_for_every_instance_and_dump(filename: str = "output.csv") -> None:
    df: pd.DataFrame = pd.DataFrame(
        columns=["algorithm", "instance", "path_weight", "time"]
    )
    for file in os.listdir(EUC_2D_DIR):
        graph = tsplib95.load(f"{EUC_2D_DIR}/{file}").get_graph()
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
        # start: float = time.perf_counter()
        # path = christofides(graph)
        # weight = networkx.path_weight(graph, path, "weight")
        # end: float = time.perf_counter()
        # df = pd.concat(
        #     [
        #         pd.DataFrame(
        #             [["christofides", file, weight, end - start]], columns=df.columns
        #         ),
        #         df,
        #     ],
        #     ignore_index=True,
        # )
    df.to_csv(filename)
