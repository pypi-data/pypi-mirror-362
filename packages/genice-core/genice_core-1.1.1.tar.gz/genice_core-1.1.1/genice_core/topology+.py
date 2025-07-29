"""
Arrange edges appropriately.

どうもバグを入れてしまったらしい。結果が変わる。

"""

from logging import getLogger, DEBUG
import networkx as nx
import numpy as np
from typing import Union, List, Tuple, Optional


def _trace_path(g: nx.Graph, path: List[int]) -> List[int]:
    """Trace the path in a linear or cyclic graph.

    Args:
        g (nx.Graph): A linear or a simple cyclic graph.
        path (List[int]): A given path to be extended.

    Returns:
        List[int]: The extended path or cycle.
    """
    while True:
        # look at the head of the path
        last, head = path[-2:]
        for next_node in g[head]:
            if next_node != last:
                # go ahead
                break
        else:
            # no next node
            return path
        path.append(next_node)
        if next_node == path[0]:
            # is cyclic
            return path


def _find_path(g: nx.Graph) -> List[int]:
    """Find a path in a linear or cyclic graph.

    Args:
        g (nx.Graph): A linear or a simple cyclic graph.

    Returns:
        List[int]: The path or cycle.
    """
    nodes = list(g.nodes())
    # choose one node
    head = nodes[0]
    # look neighbors
    neighbors = list(g[head])
    if len(neighbors) == 0:
        # isolated node
        return []
    elif len(neighbors) == 1:
        # head is an end node, fortunately.
        return _trace_path(g, [head, neighbors[0]])
    # look forward
    c0 = _trace_path(g, [head, neighbors[0]])

    if c0[-1] == head:
        # cyclic graph
        return c0

    # look backward
    c1 = _trace_path(g, [head, neighbors[1]])
    return c0[::-1] + c1[1:]


def _divide(g: nx.Graph, vertex: int, offset: int) -> None:
    """Divide a vertex into two vertices and redistribute edges.

    Args:
        g (nx.Graph): The graph to modify.
        vertex (int): The vertex to divide.
        offset (int): The offset for the new vertex label.
    """
    # fill by Nones if number of neighbors is less than 4
    nei = (list(g[vertex]) + [None, None, None, None])[:4]

    # two neighbor nodes that are passed away to the new node
    migrants = set(np.random.choice(nei, 2, replace=False)) - {None}

    # new node label
    newVertex = vertex + offset

    # assemble edges
    for migrant in migrants:
        g.remove_edge(migrant, vertex)
        g.add_edge(newVertex, migrant)


def noodlize(g: nx.Graph, fixed: nx.DiGraph = nx.DiGraph()) -> nx.Graph:
    """Divide each vertex of the graph and make a set of paths.

    A new algorithm suggested by Prof. Sakuma, Yamagata University.
    The vertices are divided based on their degrees and connectivity to minimize
    the number of crossings in the resulting paths.

    Args:
        g (nx.Graph): An ice-like undirected graph. All vertices must not be >4-degree.
        fixed (nx.DiGraph, optional): Specifies the edges whose direction is fixed. Defaults to an empty graph.

    Returns:
        nx.Graph: A graph made of chains and cycles.
    """
    logger = getLogger()

    g_fix = nx.Graph(fixed)  # undirected copy

    offset = len(g)

    # divided graph
    g_noodles = nx.Graph(g)
    for edge in fixed.edges():
        g_noodles.remove_edge(*edge)

    # Sort vertices by degree in descending order
    vertices = sorted(g.nodes(), key=lambda x: g.degree(x), reverse=True)

    for v in vertices:
        if g_fix.has_node(v):
            nfixed = g_fix.degree[v]
        else:
            nfixed = 0
        if nfixed == 0:
            # Choose neighbors to migrate based on their degrees
            neighbors = list(g_noodles[v])
            if len(neighbors) > 2:
                # Prefer neighbors with higher degrees to minimize crossings
                neighbors.sort(key=lambda x: g_noodles.degree(x), reverse=True)
                # Choose the two neighbors with highest degrees
                migrants = set(neighbors[:2])
                _divide(g_noodles, v, offset)

    return g_noodles


def _decompose_complex_path(path: List[int]) -> List[List[int]]:
    """Divide a complex path with self-crossings into simple cycles and paths.

    Args:
        path (List[int]): A complex path.

    Yields:
        List[int]: A short and simple path/cycle.
    """
    logger = getLogger()
    if len(path) == 0:
        return
    logger.debug(f"decomposing {path}...")
    order = dict()
    order[path[0]] = 0
    store = [path[0]]
    headp = 1
    while headp < len(path):
        node = path[headp]

        if node in order:
            # it is a cycle!
            size = len(order) - order[node]
            cycle = store[-size:] + [node]
            yield cycle

            # remove them from the order[]
            for v in cycle[1:]:
                del order[v]

            # truncate the store
            store = store[:-size]

        order[node] = len(order)
        store.append(node)
        headp += 1
    if len(store) > 1:
        yield store
    logger.debug(f"Done decomposition.")


def split_into_simple_paths(
    nnode: int,
    g_noodles: nx.Graph,
) -> List[List[int]]:
    """Set the orientations to the components.

    Args:
        nnode (int): Number of nodes in the original graph.
        g_noodles (nx.Graph): The divided graph.

    Yields:
        List[int]: A short and simple path/cycle.
    """
    for verticeSet in nx.connected_components(g_noodles):
        # a component of c is either a chain or a cycle.
        g_noodle = g_noodles.subgraph(verticeSet)

        # Find a simple path in the doubled graph
        # It must be a simple path or a simple cycle.
        path = _find_path(g_noodle)

        # Flatten then path. It may make the path self-crossing.
        flatten = [v % nnode for v in path]

        # Divide a long path into simple paths and cycles.
        yield from _decompose_complex_path(flatten)


def _remove_dummy_nodes(g: Union[nx.Graph, nx.DiGraph]) -> None:
    """Remove dummy nodes from the graph.

    Args:
        g (Union[nx.Graph, nx.DiGraph]): The graph to clean.
    """
    for i in range(-1, -5, -1):
        if g.has_node(i):
            g.remove_node(i)


def balance(
    fixed: nx.DiGraph, g: nx.Graph
) -> Tuple[Optional[nx.DiGraph], List[List[int]]]:
    """Extend the prefixed digraph to make the remaining graph balanced.

    Args:
        fixed (nx.DiGraph): Fixed edges.
        g (nx.Graph): Skeletal graph.

    Returns:
        Tuple[Optional[nx.DiGraph], List[List[int]]]: A tuple containing:
            - The extended fixed graph (derived cycles are included)
            - A list of derived cycles.
    """

    def _choose_free_edge(g: nx.Graph, dg: nx.DiGraph, node: int) -> Optional[int]:
        """Find an unfixed edge of the node.

        Args:
            g (nx.Graph): The original graph.
            dg (nx.DiGraph): The directed graph.
            node (int): The node to find edges for.

        Returns:
            Optional[int]: A free edge if found, None otherwise.
        """
        # add dummy nodes to make number of edges be four.
        neis = (list(g[node]) + [-1, -2, -3, -4])[:4]
        # and select one randomly
        np.random.shuffle(neis)
        for nei in neis:
            if not (dg.has_edge(node, nei) or dg.has_edge(nei, node)):
                return nei
        return None

    def _try_balance(
        _fixed: nx.DiGraph,
        in_peri: set,
        out_peri: set,
        derived_cycles: List[List[int]],
        max_attempts: int = 100,
    ) -> Tuple[Optional[nx.DiGraph], List[List[int]]]:
        """Try to balance the graph with backtracking.

        Args:
            _fixed (nx.DiGraph): The current fixed edges.
            in_peri (set): Set of nodes with more incoming edges.
            out_peri (set): Set of nodes with more outgoing edges.
            derived_cycles (List[List[int]]): List of derived cycles.
            max_attempts (int, optional): Maximum number of attempts. Defaults to 100.

        Returns:
            Tuple[Optional[nx.DiGraph], List[List[int]]]: The balanced graph and derived cycles if successful, None otherwise.
        """
        if len(out_peri) == 0 and len(in_peri) == 0:
            return _fixed, derived_cycles

        if max_attempts <= 0:
            return None, None

        # Try to balance from out_peri first
        if len(out_peri) > 0:
            node = np.random.choice(list(out_peri))
            out_peri -= {node}
            path = [node]
            while True:
                if node < 0:
                    logger.debug(f"Dead end at {node}. Path is {path}.")
                    break
                if node in in_peri:
                    logger.debug(f"Reach at a perimeter node {node}. Path is {path}.")
                    in_peri -= {node}
                    break
                if node in out_peri:
                    logger.debug(f"node {node} is on the out_peri...")
                if max(_fixed.in_degree(node), _fixed.out_degree(node)) * 2 > 4:
                    break
                next_node = _choose_free_edge(g, _fixed, node)
                if next_node is None:
                    break
                _fixed.add_edge(node, next_node)
                if next_node >= 0:
                    path.append(next_node)
                    if _fixed.in_degree(node) > _fixed.out_degree(node):
                        out_peri.add(node)
                node = next_node
                try:
                    loc = path[:-1].index(node)
                    derived_cycles.append(path[loc:])
                    path = path[: loc + 1]
                except ValueError:
                    pass
            # Try to balance the remaining graph
            result = _try_balance(
                _fixed, in_peri, out_peri, derived_cycles, max_attempts - 1
            )
            if result[0] is not None:
                return result
        # If out_peri balancing failed, try in_peri
        if len(in_peri) > 0:
            node = np.random.choice(list(in_peri))
            in_peri -= {node}
            logger.debug(
                f"first node {node}, its neighbors {g[node]} {list(_fixed.successors(node))} {list(_fixed.predecessors(node))}"
            )
            path = [node]
            while True:
                if node < 0:
                    logger.debug(f"Dead end at {node}. Path is {path} {in_peri}.")
                    break
                if node in out_peri:
                    logger.debug(f"Reach at a perimeter node {node}. Path is {path}.")
                    out_peri -= {node}
                    break
                if node in in_peri:
                    logger.debug(f"node {node} is on the in_peri...")
                if max(_fixed.in_degree(node), _fixed.out_degree(node)) * 2 > 4:
                    break
                next_node = _choose_free_edge(g, _fixed, node)
                if next_node is None:
                    break
                if next_node >= 0:
                    path.append(next_node)
                _fixed.add_edge(next_node, node)
                if next_node >= 0:
                    if _fixed.in_degree(node) < _fixed.out_degree(node):
                        in_peri.add(node)
                        logger.debug(
                            f"{node} is added to in_peri {_fixed.in_degree[node]} . {_fixed.out_degree[node]}"
                        )
                node = next_node
                try:
                    loc = path[:-1].index(node)
                    derived_cycles.append(path[loc:])
                    path = path[: loc + 1]
                except ValueError:
                    pass
            # Try to balance the remaining graph
            result = _try_balance(
                _fixed, in_peri, out_peri, derived_cycles, max_attempts - 1
            )
            if result[0] is not None:
                return result

        return None, None

    logger = getLogger()

    # Make a copy to keep the original graph untouched
    _fixed = nx.DiGraph(fixed)

    in_peri = set()
    out_peri = set()
    for node in _fixed:
        # If the node has unfixed edges,
        if _fixed.in_degree[node] + _fixed.out_degree[node] < g.degree[node]:
            # if it is not balanced,
            if _fixed.in_degree[node] > _fixed.out_degree[node]:
                out_peri.add(node)
            elif _fixed.in_degree[node] < _fixed.out_degree[node]:
                in_peri.add(node)

    logger.debug(f"out_peri {out_peri}")
    logger.debug(f"in_peri {in_peri}")

    derived_cycles: List[List[int]] = []
    result = _try_balance(_fixed, in_peri, out_peri, derived_cycles)

    if result[0] is None:
        logger.info("Failed to balance the graph.")
        return None, None

    _fixed, derived_cycles = result

    if logger.isEnabledFor(DEBUG):
        logger.debug(f"size of g {g.number_of_edges()}")
        logger.debug(f"size of fixed {_fixed.number_of_edges()}")
        assert len(in_peri) == 0, f"In-peri remains. {in_peri}"
        assert len(out_peri) == 0, f"Out-peri remains. {out_peri}"
        logger.debug("re-check perimeters")

        in_peri = set()
        out_peri = set()
        for node in _fixed:
            if node >= 0:
                if _fixed.in_degree[node] + _fixed.out_degree[node] < g.degree[node]:
                    if _fixed.in_degree[node] > _fixed.out_degree[node]:
                        out_peri.add(node)
                    elif _fixed.in_degree[node] < _fixed.out_degree[node]:
                        in_peri.add(node)

        assert len(in_peri) == 0, f"In-peri remains. {in_peri}"
        assert len(out_peri) == 0, f"Out-peri remains. {out_peri}"

        # Verify that the extended graph contains all fixed edges
        for edge in fixed.edges():
            assert _fixed.has_edge(*edge)

    _remove_dummy_nodes(_fixed)

    if logger.isEnabledFor(DEBUG):
        logger.debug(f"Number of fixed edges is {_fixed.size()} / {g.size()}")
        logger.debug(f"Number of free cycles: {len(derived_cycles)}")
        ne = sum([len(cycle) - 1 for cycle in derived_cycles])
        logger.debug(f"Number of edges in free cycles: {ne}")

    return _fixed, derived_cycles
