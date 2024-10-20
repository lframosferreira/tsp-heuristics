import sys

import networkx as nx
import tsplib95

from algorithms import christofides, twice_around_the_tree
from util import get_time_for_every_instance_and_dump


def main() -> None:
    # a = tsplib95.load("instances/EUC_2D/kroE100.tsp")
    # b = a.get_edges()
    get_time_for_every_instance_and_dump("twice_around_the_tree")


if __name__ == "__main__":
    main()
