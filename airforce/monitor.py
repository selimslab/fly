from typing import Dict, List, Set

import pandas as pd
from .api import SpireApiClient, api_client
from .plotter import TargetPlotter
from .spec import Target
from .stats import TargetStats

import threading

class SpireApiMonitor:
    stats = TargetStats()
    plotter = TargetPlotter()

    def __init__(self, api_client:SpireApiClient):
        self.api_client = api_client

    def process_target_updates(self):
        for target_json in self.api_client.streaming_target_generator():
            if target_json:
                self.stats.add_target(target_json)

    def print_stats(self):
        # pprint(asdict(self.stats))
        print(self.stats)

    def plot(self):
        self.plotter.plot_targets(self.stats.targets_seen)


# singleton 
monitor = SpireApiMonitor(api_client)
