import networkx as nx
from math import sqrt


def parse_input_file(path: str) -> nx.Graph:
    graph: nx.Graph = nx.Graph()
    with open(path, "r") as file:
        lines = file.readlines()
        number_of_nodes: int = int(lines[3].split(":")[1])
        coordinates: list[tuple[int, ...]] = [(-1, -1)]
        for line in lines[6:]:
            coordinates.append(tuple(map(lambda x: int(x), line.split(" ")[1:])))
        for i in range(1, number_of_nodes + 1):
            for j in range(i + 1, number_of_nodes + 1):
                c1: tuple[int, ...] = coordinates[i]
                c2: tuple[int, ...] = coordinates[j]
                dist: float = sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
                graph.add_edge(i, j, weight=dist)
    return graph
