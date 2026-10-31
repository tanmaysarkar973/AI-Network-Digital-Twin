
import networkx as nx
import matplotlib.pyplot as plt

from topology import NetworkTopology


network = NetworkTopology()
G = network.graph

# Position the network devices
positions = nx.spring_layout(G, seed=42)

# Assign colors based on device type
colors = []

for node in G.nodes():

    device_type = G.nodes[node]["type"]

    if device_type == "Router":
        colors.append("red")

    elif device_type == "Switch":
        colors.append("orange")

    elif device_type == "Server":
        colors.append("green")

    else:
        colors.append("skyblue")


plt.figure(figsize=(12, 8))

nx.draw(
    G,
    positions,
    with_labels=True,
    node_color=colors,
    node_size=2500,
    font_size=10,
    font_weight="bold"
)

plt.title("AI Network Digital Twin - Virtual Topology")

plt.savefig("results/network_topology.png")

plt.show()
