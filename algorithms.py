import networkx as nx
import numpy as np


# Constructive algorithms


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


# Metaheuristic


def performe_monte_carlo_steps(
    number_of_monte_carlo_steps: np.int_,
    number_of_cities: np.int_,
    temperature: np.float_,
    graph: np.array,
    nodes: np.array,
    current_path: np.array,
    current_path_cost: np.float_,
) -> np.float_:
    for _ in range(number_of_monte_carlo_steps):
        for _ in range(number_of_cities):
            proposed_x, proposed_y = np.sort(
                np.random.choice(np.arange(number_of_cities), size=2, replace=False)
            )
            current_path = np.roll(current_path, shift=1)
            proposed_path: np.array = current_path.copy()
            proposed_path[proposed_x + 1 : proposed_y] = np.flip(
                proposed_path[proposed_x + 1 : proposed_y]
            )

            remove_edge_1_cost: np.float_ = graph[current_path[proposed_x]][
                current_path[(proposed_x + 1) % number_of_cities]
            ]
            remove_edge_2_cost: np.float_ = graph[current_path[proposed_y - 1]][
                current_path[proposed_y]
            ]
            add_edge_1_cost: np.float_ = graph[proposed_path[proposed_x]][
                proposed_path[(proposed_x + 1) % number_of_cities]
            ]
            add_edge_2_cost: np.float_ = graph[proposed_path[proposed_y - 1]][
                proposed_path[proposed_y]
            ]

            decrease: np.float_ = remove_edge_1_cost + remove_edge_2_cost
            increase: np.float_ = add_edge_1_cost + add_edge_2_cost
            proposed_path_cost: np.float_ = current_path_cost - decrease + increase
            delta: np.float_ = proposed_path_cost - current_path_cost
            r: np.float_ = np.random.rand()
            P: np.float_ = np.exp(-1 * delta / temperature)
            if delta < 0 or r <= P:
                current_path = proposed_path.copy()
                current_path_cost = proposed_path_cost
    return current_path, current_path_cost


def simulated_annealing(graph: np.array) -> None:
    pass
