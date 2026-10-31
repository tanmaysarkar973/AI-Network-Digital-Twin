
import pytest

from network.topology import NetworkTopology

from digital_twin.twin_engine import DigitalTwinEngine


@pytest.fixture
def twin():

    topology = NetworkTopology()

    return DigitalTwinEngine(topology)


def test_initial_network_health(twin):

    health = twin.get_network_health()

    assert health["total_devices"] == 10
    assert health["reachable_devices"] == 10
    assert health["health_status"] == "Healthy"


def test_switch_failure(twin):

    twin.fail_device("S1")

    health = twin.get_network_health()

    assert health["health_status"] == "Degraded"
    assert health["reachable_devices"] == 1

    assert "PC1" in health["unreachable"]
    assert "Server1" in health["unreachable"]


def test_switch_recovery(twin):

    twin.fail_device("S1")
    twin.recover_device("S1")

    health = twin.get_network_health()

    assert health["reachable_devices"] == 10
    assert health["health_status"] == "Healthy"


def test_link_failure(twin):

    twin.fail_link("S1", "S2")

    health = twin.get_network_health()

    assert health["health_status"] == "Degraded"
    assert health["reachable_devices"] == 6


def test_link_recovery(twin):

    twin.fail_link("S1", "S2")
    twin.recover_link("S1", "S2")

    health = twin.get_network_health()

    assert health["reachable_devices"] == 10
    assert health["health_status"] == "Healthy"


def test_invalid_device(twin):

    with pytest.raises(ValueError):

        twin.fail_device("UNKNOWN")


def test_invalid_link(twin):

    with pytest.raises(ValueError):

        twin.fail_link("PC1", "Server1")
