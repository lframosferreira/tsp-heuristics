import networkx as nx


def parse_input_file(path: str) -> nx.Graph:
    graph: nx.Graph = nx.Graph()
    with open(path, "r") as file:
        lines = file.readlines()
        number_of_nodes: int = int(lines[3].split(":")[1])
        coordinates: list[tuple[int, ...]] = []
        for line in lines[6:]:
            coordinates.append(tuple(map(lambda x: int(x), line.split(" "))))
        for i, c1 in enumerate(coordinates):
            for j, c2 in enumreate(coordinates):
                

    return graph
