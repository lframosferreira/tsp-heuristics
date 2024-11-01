import numpy as np
import pandas as pd
import networkx
import os
import time
from util import get_graph_from_tsplib95_file

NUMBER_OF_EXECUTIONS: int = 20
INSTANCES_FOLDER: str = "instances/tsplib95"


def performe_monte_carlo_steps(
    number_of_monte_carlo_steps,
    number_of_cities,
    temperature,
    graph,
    current_path,
    current_path_cost,
):
    for _ in range(number_of_monte_carlo_steps):
        for _ in range(number_of_cities):
            proposed_x, proposed_y = np.sort(
                np.random.choice(np.arange(number_of_cities), size=2, replace=False)
            )
            current_path = np.roll(current_path, shift=1)
            proposed_path = current_path.copy()
            proposed_path[proposed_x + 1 : proposed_y] = np.flip(
                proposed_path[proposed_x + 1 : proposed_y]
            )

            remove_edge_1_cost = graph[current_path[proposed_x]][
                current_path[(proposed_x + 1) % number_of_cities]
            ]
            remove_edge_2_cost = graph[current_path[proposed_y - 1]][
                current_path[proposed_y]
            ]
            add_edge_1_cost = graph[proposed_path[proposed_x]][
                proposed_path[(proposed_x + 1) % number_of_cities]
            ]
            add_edge_2_cost = graph[proposed_path[proposed_y - 1]][
                proposed_path[proposed_y]
            ]

            decrease = remove_edge_1_cost + remove_edge_2_cost
            increase = add_edge_1_cost + add_edge_2_cost
            proposed_path_cost = current_path_cost - decrease + increase
            delta = proposed_path_cost - current_path_cost
            r = np.random.rand()
            P = np.exp(-1 * delta / temperature)
            if delta < 0 or r <= P:
                current_path = proposed_path.copy()
                current_path_cost = proposed_path_cost
    return current_path, current_path_cost


def tsp(graph, temperature, delta_t, temperature_inferior_limit):
    number_of_monte_carlo_steps = 1  # hard coded
    number_of_cities = graph.shape[0]
    current_path = np.arange(number_of_cities)
    np.random.shuffle(current_path)
    edges = np.append(
        np.lib.stride_tricks.sliding_window_view(current_path, 2),
        [[current_path[-1], current_path[0]]],
        axis=0,
    )
    current_path_cost = np.sum([graph[i, j] for i, j in edges])

    temperatures = []
    distances = []

    while temperature > temperature_inferior_limit:
        temperatures.append(temperature)
        distances.append(current_path_cost)
        current_path, current_path_cost = performe_monte_carlo_steps(
            number_of_monte_carlo_steps=number_of_monte_carlo_steps,
            number_of_cities=number_of_cities,
            temperature=temperature,
            graph=graph,
            current_path=current_path,
            current_path_cost=current_path_cost,
        )
        temperature *= delta_t

    current_path = np.append(current_path, current_path[0])
    return current_path, current_path_cost, distances, temperatures


# initial config (can be changed)
TEMPERATURE = 10.0
DELTA_T = 0.9
TEMPERATURE_INFERIOR_LIMIT = 0.10


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
        total_time: float = 0.0
        weight: int = 0
        for _ in range(NUMBER_OF_EXECUTIONS):
            start: float = time.perf_counter()
            path, cost, _, _ = tsp(
                graph=graph,
                temperature=TEMPERATURE,
                delta_t=DELTA_T,
                temperature_inferior_limit=TEMPERATURE_INFERIOR_LIMIT,
            )
            path += 1
            weight = cost
            end: float = time.perf_counter()
            total_time += end - start
        df = pd.concat(
            [
                pd.DataFrame(
                    [["sa", file, weight, total_time / NUMBER_OF_EXECUTIONS]],
                    columns=df.columns,
                ),
                df,
            ],
            ignore_index=True,
        )

    df.to_csv(filename)
