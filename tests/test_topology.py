
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from network.topology import NetworkTopology


def test_total_devices():
    network = NetworkTopology()
    assert network.graph.number_of_nodes() == 10


def test_total_connections():
    network = NetworkTopology()
    assert network.graph.number_of_edges() == 9


def test_router_exists():
    network = NetworkTopology()
    assert "R1" in network.graph.nodes


def test_servers_exist():
    network = NetworkTopology()
    assert "Server1" in network.graph.nodes
    assert "Server2" in network.graph.nodes


def test_network_connected():
    network = NetworkTopology()
    assert nx.is_connected(network.graph)


import networkx as nx
