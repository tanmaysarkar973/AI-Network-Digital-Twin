
from datetime import datetime, timezone


class NetworkState:

    def __init__(self):
        self.devices = {}
        self.links = {}
        self.last_updated = None

    def update_device(self, device_id, status):

        self.devices[device_id] = {
            "status": status,
            "last_updated": datetime.now(
                timezone.utc
            ).isoformat()
        }

        self.last_updated = datetime.now(
            timezone.utc
        ).isoformat()

    def update_link(self, source, destination, status):

        link_id = tuple(sorted((source, destination)))

        self.links[link_id] = {
            "status": status,
            "last_updated": datetime.now(
                timezone.utc
            ).isoformat()
        }

        self.last_updated = datetime.now(
            timezone.utc
        ).isoformat()

    def get_snapshot(self):

        return {
            "devices": self.devices.copy(),
            "links": {
                f"{source}-{destination}": details
                for (source, destination), details
                in self.links.items()
            },
            "last_updated": self.last_updated
        }
