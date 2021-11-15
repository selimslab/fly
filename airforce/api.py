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
        self.api_url = update_url_query_params(
            self.api_url, {"position_token": self.last_seen_position_token}
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

    token = "eyIwIjoxNDM3NTE0Njk5LCIxIjoxMzg4NzI0MjExLCIyIjoxNDM4NzIyOTU5LCIzIjoxNDc1ODk5MzA4LCI0IjoxNDE4NTk3MzYxLCI1IjoxMzkzMjgzNTQyLCI2IjoxNDk3NzgxMzQxLCI3IjoxNDE2NDIzMzUyLCI4IjoxNDc2ODExMTg5LCI5IjoxMzk2NjI1MzAxLCIxMCI6MTQ1NDUwNDQ3MiwiMTEiOjE0MzI0MjA4OTgsIjEyIjoxNDU1MDMxMTY4LCIxMyI6MTUyODU2NzU3NiwiMTQiOjE0MzQzNzEwMDEsIjE1IjoxNDM0MzQ0MzM2LCIxNiI6MTUwNjEwMTA2MywiMTciOjE0NzIzNzcxNzMsIjE4IjoxNTM4OTI3MzQ4LCIxOSI6MTQ3NTYzMTM3OSwiMjAiOjEzNDgwMjU5NjIsIjIxIjoxNDIzNDg0MDQ4LCIyMiI6MTQ3NDQxOTgzMiwiMjMiOjE0ODE5NjkwMDAsIjI0IjoxNDcyOTk0ODk4LCIyNSI6MTM5MDU2MzIyMiwiMjYiOjE0NDEzMTI0MTMsIjI3IjoxNDA5MDc2MDE1LCIyOCI6MTQ3MDcyOTk2MywiMjkiOjEzNzczNTkxMzEsIjMwIjoxNDYxNzQ3MTEyLCIzMSI6MTUwNTEwNDM0OSwiMzIiOjE0MjQ5MzQzODIsIjMzIjoxNDI0MDEwMDE0LCIzNCI6MTQxNTczNjIzNSwiMzUiOjE0NzU0NjYxMDl9"
    api_url = update_url_query_params(api_url, {"position_token": token})
    if api_url and api_auth_token:
        api_client = TrackingStreamClient(api_url, api_auth_token)
        return api_client
    else:
        raise Exception("please make sure you have API_URL and API_TOKEN in .env")


# singleton
tracking_stream_api_client = create_spire_api_client()
