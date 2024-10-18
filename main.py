from algorithms import twice_around_the_tree
import networkx as nx
from util import parse_input_file


def main() -> None:
    print("Hello TSP")
    graph: nx.Graph = parse_input_file("instances/EUC_2D/pr76.tsp")
    print(graph)


if __name__ == "__main__":
    main()
