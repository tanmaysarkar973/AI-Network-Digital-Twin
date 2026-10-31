
from network.topology import NetworkTopology

from digital_twin.twin_engine import DigitalTwinEngine


def display_health(engine, title):

    health = engine.get_network_health()

    print("\n" + "=" * 55)
    print(title)
    print("=" * 55)

    print("Network Status:", health["health_status"])
    print("Health Score:", health["health_score"], "%")

    print(
        "Online Devices:",
        health["online_devices"],
        "/",
        health["total_devices"]
    )

    print("Reachable Devices:", health["reachable_devices"])

    print("Unreachable Devices:", health["unreachable_devices"])

    print("Active Links:", health["active_links"])

    print("Unavailable Links:", health["failed_links"])

    print("Reachable:", health["reachable"])

    print("Unreachable:", health["unreachable"])


def main():

    # Create original virtual topology
    topology = NetworkTopology()

    # Initialize Digital Twin
    twin = DigitalTwinEngine(topology)

    # Scenario 1: Normal network
    display_health(
        twin,
        "SCENARIO 1: NORMAL NETWORK"
    )

    # Scenario 2: Switch failure
    twin.fail_device("S1")

    display_health(
        twin,
        "SCENARIO 2: SWITCH S1 FAILURE"
    )

    # Scenario 3: Recover switch
    twin.recover_device("S1")

    display_health(
        twin,
        "SCENARIO 3: SWITCH S1 RECOVERY"
    )

    # Scenario 4: Link failure
    twin.fail_link("S1", "S2")

    display_health(
        twin,
        "SCENARIO 4: LINK FAILURE"
    )

    # Scenario 5: Link recovery
    twin.recover_link("S1", "S2")

    display_health(
        twin,
        "SCENARIO 5: LINK RECOVERY"
    )

    # Show final virtual state
    print("\n===== DIGITAL TWIN SNAPSHOT =====")

    print(twin.get_network_snapshot())


if __name__ == "__main__":
    main()
