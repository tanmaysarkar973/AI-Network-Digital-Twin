
import networkx as nx

from digital_twin.network_state import NetworkState


class DigitalTwinEngine:

    def __init__(self, topology):

        self.graph = topology.graph
        self.state = NetworkState()

        # Initialize virtual device states
        for device in self.graph.nodes:

            self.graph.nodes[device]["status"] = "Online"

            self.state.update_device(
                device,
                "Online"
            )

        # Initialize virtual connection states
        for source, destination in self.graph.edges:

            self.graph.edges[source, destination]["status"] = "Up"

            self.state.update_link(
                source,
                destination,
                "Up"
            )

    def fail_device(self, device_id):

        if device_id not in self.graph:
            raise ValueError(
                f"Unknown device: {device_id}"
            )

        self.graph.nodes[device_id]["status"] = "Offline"

        self.state.update_device(
            device_id,
            "Offline"
        )

        print(f"[FAILURE] Device {device_id} is offline.")

    def recover_device(self, device_id):

        if device_id not in self.graph:
            raise ValueError(
                f"Unknown device: {device_id}"
            )

        self.graph.nodes[device_id]["status"] = "Online"

        self.state.update_device(
            device_id,
            "Online"
        )

        print(f"[RECOVERY] Device {device_id} is online.")

    def fail_link(self, source, destination):

        if not self.graph.has_edge(source, destination):
            raise ValueError(
                f"Connection {source}-{destination} does not exist."
            )

        self.graph.edges[source, destination]["status"] = "Down"

        self.state.update_link(
            source,
            destination,
            "Down"
        )

        print(
            f"[FAILURE] Link {source} - {destination} is down."
        )

    def recover_link(self, source, destination):

        if not self.graph.has_edge(source, destination):
            raise ValueError(
                f"Connection {source}-{destination} does not exist."
            )

        self.graph.edges[source, destination]["status"] = "Up"

        self.state.update_link(
            source,
            destination,
            "Up"
        )

        print(
            f"[RECOVERY] Link {source} - {destination} is restored."
        )

    def get_active_graph(self):

        active_graph = nx.Graph()

        # Include online devices only
        for device, attributes in self.graph.nodes(data=True):

            if attributes["status"] == "Online":

                active_graph.add_node(
                    device,
                    **attributes
                )

        # Include active connections only
        for source, destination, attributes in self.graph.edges(data=True):

            if (
                attributes["status"] == "Up"
                and source in active_graph
                and destination in active_graph
            ):

                active_graph.add_edge(
                    source,
                    destination,
                    **attributes
                )

        return active_graph

    def get_reachable_devices(self, source="R1"):

        active_graph = self.get_active_graph()

        if source not in active_graph:
            return []

        return sorted(
            nx.node_connected_component(
                active_graph,
                source
            )
        )

    def get_network_health(self):

        active_graph = self.get_active_graph()

        total_devices = self.graph.number_of_nodes()

        total_links = self.graph.number_of_edges()

        online_devices = [
            device
            for device, data in self.graph.nodes(data=True)
            if data["status"] == "Online"
        ]

        active_links = [
            (u, v)
            for u, v, data in self.graph.edges(data=True)
            if data["status"] == "Up"
            and u in active_graph
            and v in active_graph
        ]

        reachable = self.get_reachable_devices()

        unreachable = sorted(
            set(self.graph.nodes) - set(reachable)
        )

        health_score = (
            len(reachable) / total_devices * 100
            if total_devices else 0
        )

        if len(reachable) == total_devices:
            health_status = "Healthy"

        elif reachable:
            health_status = "Degraded"

        else:
            health_status = "Critical"

        return {
            "total_devices": total_devices,
            "online_devices": len(online_devices),
            "reachable_devices": len(reachable),
            "unreachable_devices": len(unreachable),
            "total_links": total_links,
            "active_links": len(active_links),
            "failed_links": total_links - len(active_links),
            "health_score": round(health_score, 2),
            "health_status": health_status,
            "reachable": reachable,
            "unreachable": unreachable
        }

    def get_network_snapshot(self):

        return self.state.get_snapshot()
