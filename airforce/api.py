import json
import os
from dataclasses import dataclass
from typing import Optional

import requests
from dotenv import load_dotenv

from .util.logger import logger
from .util.url import update_url_query_params


@dataclass
class StreamingApiClient:
    api_url: str
    api_auth_token: str

    def stream_generator(self):
        headers = {"Authorization": f"Bearer {self.api_auth_token}"}

        with requests.get(self.api_url, stream=True, headers=headers) as r:
            if r.encoding is None:
                r.encoding = "utf-8"

            for line in r.iter_lines():
                # filter out keep-alive new lines
                if line:
                    line = json.loads(line)
                    yield line


@dataclass
class TrackingStreamClient(StreamingApiClient):

    last_seen_position_token: Optional[str] = None

    def continue_from_remaining_position(self):
        self.api_url += update_url_query_params(
            self.api_url, {"token": self.last_seen_position_token}
        )
        self.target_update_generator()

    def target_update_generator(self):
        try:
            for line in self.stream_generator():
                if "positionToken" in line:
                    token = line["positionToken"]
                    # self.last_processed_position_token = self.last_seen_position_token
                    self.last_seen_position_token = token
                    yield
                elif "target" in line:
                    target = line["target"]
                    yield target
        except Exception as e:
            # connection lost, recover
            logger.error(e)
            self.continue_from_remaining_position()


def create_spire_api_client() -> TrackingStreamClient:
    load_dotenv()
    api_url = os.getenv("API_URL")
    api_auth_token = os.getenv("API_TOKEN")
    if api_url and api_auth_token:
        api_client = TrackingStreamClient(api_url, api_auth_token)
        return api_client
    else:
        raise Exception("please make sure you have API_URL and API_TOKEN in .env")


# singleton
tracking_stream_api_client = create_spire_api_client()
