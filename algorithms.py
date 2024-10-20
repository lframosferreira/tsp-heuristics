import networkx as nx


def twice_around_the_tree(graph: nx.Graph, dfs_src_node: int = 1) -> list[int]:
    mst: nx.Graph = nx.minimum_spanning_tree(graph)
    hamiltonian_cycle: list[int] = list(nx.dfs_preorder_nodes(mst, source=dfs_src_node))
    return hamiltonian_cycle + [dfs_src_node]


def christofides(graph: nx.Graph, src: int = 1):
    mst = nx.minimum_spanning_tree(graph)
    odd_degre_nodes: list[int] = []
    for node in mst.nodes:
        if mst.degree[node] % 2 == 1:
            odd_degre_nodes.append(node)
    induced_subgraph = graph.subgraph(odd_degre_nodes)
    min_weight_perfect_matching = nx.min_weight_matching(induced_subgraph)
    eulerian_multigraph: nx.MultiGraph = nx.MultiGraph(mst)
    eulerian_multigraph.add_edges_from(min_weight_perfect_matching)
    eulerian_circuit = list(nx.eulerian_circuit(eulerian_multigraph))
    hamiltonian_cycle = []
    for u, _ in eulerian_circuit:
        if u in hamiltonian_cycle:
            continue
        hamiltonian_cycle.append(u)
    return hamiltonian_cycle + [src]
