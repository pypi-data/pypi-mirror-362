import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class RequestsSessionManager:
    def __init__(self, retry: Retry):
        self._retry = retry

    def __enter__(self):
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=self._retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        self._session = session
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
