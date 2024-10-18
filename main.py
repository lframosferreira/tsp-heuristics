from algorithms import twice_around_the_tree
import networkx as nx
from util import parse_input_file


def main() -> None:
    print("Hello TSP")
    graph: nx.Graph = parse_input_file("instances/EUC_2D/pr76.tsp")
    print(graph.get_edge_data(1, 2))


if __name__ == "__main__":
    main()
