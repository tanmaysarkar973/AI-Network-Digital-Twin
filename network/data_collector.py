
import csv
import json
import os


class NetworkDataCollector:

    def __init__(self, output_dir="dataset"):

        self.output_dir = output_dir

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

    def save_packets(self, records):

        filepath = os.path.join(
            self.output_dir,
            "network_traffic.csv"
        )

        if not records:
            print("No packet records available.")
            return

        with open(
            filepath,
            "w",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=records[0].keys()
            )

            writer.writeheader()
            writer.writerows(records)

        print(f"Packet dataset saved: {filepath}")

    def save_metrics(self, metrics):

        filepath = os.path.join(
            self.output_dir,
            "network_metrics.json"
        )

        with open(filepath, "w") as file:

            json.dump(
                metrics,
                file,
                indent=4
            )

        print(f"Network metrics saved: {filepath}")
