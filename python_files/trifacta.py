"""
Class to maintain methods which interact with Trifacta via the API
"""
import logging
from typing import Dict, List
import json
import requests
from requests import Request, Session
import pandas as pd


# Quick helper not included in requests
# https://github.com/psf/requests/issues/4437
class HTTPBearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        return self.token == getattr(other, 'token', None)

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r


class TrifactaClient:
    def __init__(self, *, host: str, token: str, logger=None):
        self.host = host
        self.token = token
        self.session = Session()
        self.session.auth = HTTPBearerAuth(self.token)
        self.logger = logger or logging.getLogger(__name__)

    def call_api(self, request: requests.Request):
        prepared_request = self.session.prepare_request(request)
        response = self.session.send(prepared_request)  # TODO: implement retry
        try:
            response.raise_for_status()
        except requests.HTTPError:
            self.logger.error(f'HTTP Error with content:\n{response.text}')
            raise
        except requests.exceptions.RequestException:
            self.logger.exception('Failed to get a reply from the API')
            raise
        except Exception:
            raise
        return response

    def get_flows(self) -> Dict:
        endpoint = 'v4/flows'
        request = Request('GET', self.host + endpoint)
        response = self.call_api(request)
        return response.json()

    def list_flows(self) -> List[Dict]:
        """List all Flows"""
        return self.get_flows()['data']

    def get_flow_ids_by_name(self) -> Dict[str, int]:
        """Get a dict of flows name to id mapping"""
        return {flow['name']: flow['id'] for flow in self.list_flows()}

    def get_flow_id(self, name: str) -> int:
        """Lookup a flow's id using its name"""
        flows = self.get_flow_ids_by_name()
        if name not in flows:
            raise KeyError(f'{name} not found in flows')
        return flows[name]

    def upload_dataset(self, file_path: str, name:str) -> int:
        """Upload a dataset to trifacta and store its id."""
        endpoint = 'v4/importedDatasets'
        data = json.dumps({
            "uri": 's3://'+file_path,
            "name": name,
            "detectStructure": True
        })
        request = Request('POST', self.host+endpoint, json=data, headers={'Content-type':'application/json'})

        response = self.call_api(request)
        return response['id']

    def replace_dataset(self, flow_id: int, old_id: int, new_id: int) -> None:
        """Patch a recipe and change the input dataset."""
        endpoint = f'v4/flows/{flow_id}/replaceDataset'
        data = json.dumps({
            "importedDatasetId": old_id,
            "newImportedDatasetId": new_id
        })
        print('data',data)
        
        
        request = Request('PATCH', self.host+endpoint, data=data, headers={'Content-type':'application/json'})
        self.call_api(request)
    
    def get_dataset_id_by_name(self, flow_id: int, dataset_name: str) -> None:
        """Get a dataset id by checking for like name."""
        endpoint = f'v4/flows/{flow_id}/inputs'
        request = Request('GET', self.host+endpoint)
        response = self.call_api(request).json()
        for d in response['data']:
            print(d['id'], d['name'])
            if dataset_name in d['name']:
                return d['id']
        
    


        



