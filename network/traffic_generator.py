
import random
import simpy
import networkx as nx


class NetworkTrafficSimulator:

    def __init__(
        self,
        topology,
        duration=10,
        seed=42,
        packet_size=1500
    ):
        self.graph = topology.graph
        self.duration = duration
        self.packet_size = packet_size

        self.rng = random.Random(seed)
        self.env = simpy.Environment()

        self.records = []
        self.packet_counter = 0

        self.clients = [
            f"PC{i}" for i in range(1, 6)
        ]

        self.servers = ["Server1", "Server2"]

        self.links = {}

        # Create virtual network links
        for u, v in self.graph.edges():

            # Lower capacity on the switch-to-switch link
            if {u, v} == {"S1", "S2"}:
                bandwidth = 5
            else:
                bandwidth = 100

            self.links[tuple(sorted((u, v)))] = {
                "resource": simpy.Resource(
                    self.env, capacity=1
                ),
                "bandwidth_mbps": bandwidth,
                "propagation_ms": 1,
                "queue_limit": 25
            }

    def send_packet(self, packet_id, source, destination):

        sent_at = self.env.now

        try:
            path = nx.shortest_path(
                self.graph,
                source,
                destination
            )
        except nx.NetworkXNoPath:
            return

        for i in range(len(path) - 1):

            u = path[i]
            v = path[i + 1]

            link = self.links[
                tuple(sorted((u, v)))
            ]

            resource = link["resource"]

            # Check queue capacity
            if len(resource.queue) >= link["queue_limit"]:

                self.records.append({
                    "packet_id": packet_id,
                    "source": source,
                    "destination": destination,
                    "path": " -> ".join(path),
                    "packet_size_bytes": self.packet_size,
                    "latency_ms": (
                        self.env.now - sent_at
                    ) * 1000,
                    "status": "DROPPED"
                })

                return

            # Request transmission resource
            with resource.request() as request:

                yield request

                bandwidth = link["bandwidth_mbps"]

                transmission_time = (
                    self.packet_size * 8
                ) / (bandwidth * 1_000_000)

                # Transmission + propagation delay
                yield self.env.timeout(
                    transmission_time
                    + link["propagation_ms"] / 1000
                )

        latency = (self.env.now - sent_at) * 1000

        self.records.append({
            "packet_id": packet_id,
            "source": source,
            "destination": destination,
            "path": " -> ".join(path),
            "packet_size_bytes": self.packet_size,
            "latency_ms": round(latency, 4),
            "status": "DELIVERED"
        })

    def generate_traffic(self, source):

        while self.env.now < self.duration:

            interval = self.rng.uniform(0.003, 0.008)

            yield self.env.timeout(interval)

            if self.env.now > self.duration:
                break

            destination = self.rng.choice(self.servers)

            self.packet_counter += 1

            self.env.process(
                self.send_packet(
                    self.packet_counter,
                    source,
                    destination
                )
            )

    def run(self):

        # Start traffic generation from all clients
        for client in self.clients:

            self.env.process(
                self.generate_traffic(client)
            )

        # Complete traffic generation and drain queued packets
        self.env.run()

        return self.records

    def get_metrics(self):

        total = len(self.records)

        delivered = [
            p for p in self.records
            if p["status"] == "DELIVERED"
        ]

        dropped = total - len(delivered)

        latencies = [
            p["latency_ms"] for p in delivered
        ]

        actual_duration = max(
            self.env.now, 0.001
        )

        average_latency = (
            sum(latencies) / len(latencies)
            if latencies else 0
        )

        sorted_latencies = sorted(latencies)

        p95_latency = (
            sorted_latencies[
                int(0.95 * (len(sorted_latencies) - 1))
            ]
            if sorted_latencies else 0
        )

        throughput = (
            len(delivered)
            * self.packet_size
            * 8
            / actual_duration
            / 1_000_000
        )

        packet_loss = (
            dropped / total * 100
            if total else 0
        )

        return {
            "total_packets": total,
            "delivered_packets": len(delivered),
            "dropped_packets": dropped,
            "packet_loss_percent": round(packet_loss, 2),
            "average_latency_ms": round(
                average_latency, 4
            ),
            "p95_latency_ms": round(
                p95_latency, 4
            ),
            "throughput_mbps": round(
                throughput, 4
            ),
            "simulation_time_seconds": round(
                actual_duration, 4
            )
        }
