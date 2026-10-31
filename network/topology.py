
import networkx as nx


class NetworkTopology:

    def __init__(self):
        self.graph = nx.Graph()
        self.create_topology()

    def create_topology(self):

        # Router
        self.graph.add_node(
            "R1",
            type="Router",
            ip="192.168.1.1",
            status="Online"
        )

        # Switches
        self.graph.add_node(
            "S1",
            type="Switch",
            ip="192.168.1.2",
            status="Online"
        )

        self.graph.add_node(
            "S2",
            type="Switch",
            ip="192.168.1.3",
            status="Online"
        )

        # Client computers
        for i in range(1, 6):
            self.graph.add_node(
                f"PC{i}",
                type="Client",
                ip=f"192.168.1.{10+i}",
                status="Online"
            )

        # Servers
        for i in range(1, 3):
            self.graph.add_node(
                f"Server{i}",
                type="Server",
                ip=f"192.168.1.{20+i}",
                status="Online"
            )

        # Network connections
        connections = [
            ("R1", "S1"),
            ("S1", "PC1"),
            ("S1", "PC2"),
            ("S1", "PC3"),
            ("S1", "PC4"),
            ("S1", "S2"),
            ("S2", "PC5"),
            ("S2", "Server1"),
            ("S2", "Server2")
        ]

        self.graph.add_edges_from(connections)

    def get_devices(self):
        return dict(self.graph.nodes(data=True))

    def get_connections(self):
        return list(self.graph.edges())

    def display_topology(self):

        print("\n===== NETWORK DEVICES =====")

        for device, details in self.graph.nodes(data=True):
            print(
                device,
                "|",
                details["type"],
                "|",
                details["ip"],
                "|",
                details["status"]
            )

        print("\n===== NETWORK CONNECTIONS =====")

        for source, destination in self.graph.edges():
            print(source, "<---->", destination)

        print("\nTotal Devices:", self.graph.number_of_nodes())
        print("Total Connections:", self.graph.number_of_edges())


if __name__ == "__main__":

    network = NetworkTopology()

    network.display_topology()
