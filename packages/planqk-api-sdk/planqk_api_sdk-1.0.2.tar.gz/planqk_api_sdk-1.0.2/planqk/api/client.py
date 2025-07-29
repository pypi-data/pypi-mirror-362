import os
from typing import Optional

from planqk.api.credentials import DefaultCredentialsProvider
from planqk.api.sdk import PlanqkApi
from planqk.api.sdk.data_pools.client import DataPoolsClient

_PLANQK_API_BASE_URL_NAME = "PLANQK_API_BASE_URL"


class PlanqkApiClient:
    def __init__(self, access_token: Optional[str] = None):
        base_url = os.environ.get(_PLANQK_API_BASE_URL_NAME, "https://platform.planqk.de/qc-catalog")
        credentials_provider = DefaultCredentialsProvider(access_token)
        self._api = PlanqkApi(base_url=base_url, api_key=credentials_provider.get_access_token())

    @property
    def data_pools(self) -> DataPoolsClient:
        return self._api.data_pools
