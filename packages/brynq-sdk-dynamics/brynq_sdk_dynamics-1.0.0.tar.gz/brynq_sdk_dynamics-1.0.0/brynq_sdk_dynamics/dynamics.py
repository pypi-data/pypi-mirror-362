import requests
import pandas as pd
from brynq_sdk_brynq import BrynQ
from typing import Optional, Literal, Dict, Any


class Dynamics(BrynQ):
    def __init__(self, system_type: Optional[Literal['source', 'target']] = None, debug=False) -> None:
        """
        Initializes the Dynamics client, retrieves credentials, and sets authorization headers.

        """
        super().__init__()
        credentials = self.interfaces.credentials.get(system="dynamics-365", system_type=system_type)
        credentials = credentials.get('data')
        self.client_id = credentials['client_id']
        self.client_secret = credentials['client_secret']
        self.resource = credentials['resource']
        self.tenant = credentials['tenant_id']
        self.headers = {'authorization': f'Bearer {self.get_access_token()}'}
        self.timeout = 3600


    def get_access_token(self) -> str:
        """
        Retrieves an OAuth2 access token from Microsoft Azure AD.

        """
        url = f"https://login.microsoftonline.com/{self.tenant}/oauth2/token"
        payload = {'grant_type': 'client_credentials',
                   'client_id': self.client_id,
                   'client_secret': self.client_secret,
                   'resource': self.resource}
        response = requests.post(url= url, data=payload, timeout=self.timeout)
        return response.json()['access_token']

    def get_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Retrieves data from a specified Dynamics 365 OData endpoint.

        Handles pagination using '@odata.nextLink' and combines results into a single pandas DataFrame.

        """
        url = f"{self.resource}/data/{endpoint}"
        df = pd.DataFrame()

        while True:
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            df = pd.concat([df, pd.DataFrame(response.json()['value'])], ignore_index=True)

            if '@odata.nextLink' in response.json():
                url = response.json()['@odata.nextLink']
                params = None
            else:
                break

        return df


