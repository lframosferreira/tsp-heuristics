import networkx as nx


def twice_around_the_tree(graph: nx.Graph, dfs_src_node: int = 1) -> list[int]:
    mst: nx.Graph = nx.minimum_spanning_tree(graph)
    hamiltonian_cycle = list(nx.dfs_preorder_nodes(mst, source=dfs_src_node))
    return hamiltonian_cycle + [dfs_src_node]
