import json
import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv


@dataclass
class StreamingApiClient:
    api_url: str 
    api_auth_token: str 

    def stream_generator(self):
        # TODO - add error handling 
        headers={'Authorization': f'Bearer {self.api_auth_token}'}

        with requests.get(self.api_url, stream=True, headers=headers) as r:
            if r.encoding is None:
                r.encoding = 'utf-8'

            for line in r.iter_lines():
                # filter out keep-alive new lines
                if line:
                    line = json.loads(line)
                    yield line 

@dataclass
class SpireApiClient(StreamingApiClient):
    
    def __post_init__(self):
        self.last_seen_position_token:str = None
        self.last_processed_position_token:str = None 
    
    def streaming_target_generator(self):
        for line in self.stream_generator():
            if 'positionToken' in line:
                token = line['positionToken']
                if token != self.last_seen_position_token:
                    self.last_processed_position_token = self.last_seen_position_token
                    self.last_seen_position_token = token
                    yield 
            elif 'target' in line:
                target = line['target']
                yield target 


def create_spire_api_client()->SpireApiClient:
    load_dotenv()
    api_url = os.getenv("API_URL", "") 
    api_auth_token = os.getenv("API_TOKEN", "")
    api_client = SpireApiClient(api_url, api_auth_token)
    return api_client

# singleton 
api_client = create_spire_api_client()
