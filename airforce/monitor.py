from .api import TrackingStreamClient, tracking_stream_api_client
from .plotter import TargetPlotter
from .stats import TargetStats


class TrackingStreamMonitor:
    stats = TargetStats()
    plotter = TargetPlotter()

    def __init__(self, api_client: TrackingStreamClient):
        self.api_client = api_client

    def process_target_updates(self):
        for target_json in self.api_client.target_update_generator():
            if target_json:
                self.stats.add_target(target_json)

    def print_stats(self):
        print(self.stats)

    def plot(self):
        self.plotter.plot_targets(self.stats.targets_seen)


# singleton
monitor = TrackingStreamMonitor(tracking_stream_api_client)
