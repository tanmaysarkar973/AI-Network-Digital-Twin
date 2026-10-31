
from network.topology import NetworkTopology
from network.traffic_generator import NetworkTrafficSimulator


def test_simulation_generates_packets():

    topology = NetworkTopology()

    simulator = NetworkTrafficSimulator(
        topology,
        duration=1,
        seed=42
    )

    records = simulator.run()

    assert len(records) > 0


def test_packet_status():

    topology = NetworkTopology()

    simulator = NetworkTrafficSimulator(
        topology,
        duration=1,
        seed=42
    )

    records = simulator.run()

    for packet in records:
        assert packet["status"] in [
            "DELIVERED",
            "DROPPED"
        ]


def test_metrics_are_valid():

    topology = NetworkTopology()

    simulator = NetworkTrafficSimulator(
        topology,
        duration=1,
        seed=42
    )

    simulator.run()

    metrics = simulator.get_metrics()

    assert metrics["total_packets"] > 0

    assert (
        metrics["delivered_packets"]
        + metrics["dropped_packets"]
        == metrics["total_packets"]
    )

    assert 0 <= metrics["packet_loss_percent"] <= 100
