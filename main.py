from algorithms import twice_around_the_tree
import networkx as nx


def main() -> None:
    print("Hello TSP")
    graph: nx.Graph = nx.Graph()
    for i in range(1, 4):
        graph.add_node(i)
    graph.add_edge(1, 2, weight=10)
    graph.add_edge(2, 3, weight=20)
    graph.add_edge(3, 1, weight=30)
    twice_around_the_tree(graph)


if __name__ == "__main__":
    main()
