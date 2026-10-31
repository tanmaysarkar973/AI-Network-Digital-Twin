
from network.topology import NetworkTopology

from network.traffic_generator import (
    NetworkTrafficSimulator
)

from network.data_collector import (
    NetworkDataCollector
)


def main():

    print("=" * 55)
    print(" AI NETWORK DIGITAL TWIN")
    print(" NETWORK TRAFFIC SIMULATION")
    print("=" * 55)

    # Initialize virtual topology
    topology = NetworkTopology()

    print("\nNetwork topology initialized.")

    # Initialize traffic simulator
    simulator = NetworkTrafficSimulator(
        topology=topology,
        duration=10,
        seed=42,
        packet_size=1500
    )

    print("Starting packet generation...")

    # Run simulation
    records = simulator.run()

    # Calculate metrics
    metrics = simulator.get_metrics()

    # Save results
    collector = NetworkDataCollector()

    collector.save_packets(records)
    collector.save_metrics(metrics)

    print("\n===== SIMULATION RESULTS =====")

    for key, value in metrics.items():

        print(
            f"{key.replace('_', ' ').title()}: {value}"
        )

    print("\nSimulation completed successfully!")


if __name__ == "__main__":
    main()
