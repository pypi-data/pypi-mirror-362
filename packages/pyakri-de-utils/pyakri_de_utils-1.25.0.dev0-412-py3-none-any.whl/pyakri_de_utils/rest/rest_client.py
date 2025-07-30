from typing import Any, List, Optional

from urllib3 import Retry
from requests import HTTPError
from pyakri_de_utils import logger
from pyakri_de_utils.rest.exceptions import (
    RestClientHTTPException,
    RestClientException,
)
from pyakri_de_utils.rest.models import RestResponse
from pyakri_de_utils.rest.requests_session_manager import RequestsSessionManager


class RestClient:
    def __init__(self, retry: Retry):
        self._retry = retry

    @staticmethod
    def get_client(retry: Retry):
        return RestClient(retry=retry)

    def exec_post_request(
        self,
        url: str,
        body: Optional[dict] = None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        file_paths: Optional[List[str]] = None,
    ) -> RestResponse:
        return self.exec_request(
            url=url,
            body=body,
            params=params,
            headers=headers,
            method="post",
            file_paths=file_paths,
        )

    def exec_get_request(
        self,
        url: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> RestResponse:
        return self.exec_request(url=url, params=params, headers=headers, method="get")

    def _exec_request(
        self,
        url: str,
        method: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
        files: Optional[List[Any]] = None,
    ):
        with RequestsSessionManager(retry=self._retry) as session:
            try:
                with session.request(
                    method=method,
                    url=url,
                    data=body,
                    headers=headers,
                    params=params,
                    files=files,
                ) as response:
                    status_code = response.status_code
                    message = response.reason
                    json_data = None
                    if response.text:
                        try:
                            json_data = response.json()
                        except Exception as err:
                            logger.error(f"JSON decode failed with err {err}")
                            raise RestClientException(message=str(err))

                    if not (200 <= status_code <= 299):
                        raise RestClientException(
                            message=message, status_code=status_code
                        )

                    return RestResponse(
                        status_code=status_code,
                        json_data=json_data,
                        message=message,
                    )
            except HTTPError as http_err:
                status_code = (
                    http_err.response.status_code if http_err.response else 500
                )
                logger.error("HTTP error occurred: %s", str(http_err))
                raise RestClientHTTPException(
                    status_code=status_code, message=str(http_err)
                )
            except Exception as exp:
                logger.error(f"Failed to send request due to {exp}")
                raise RestClientException(message=str(exp))

    def exec_request(
        self,
        url: str,
        method: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
        file_paths: Optional[List[str]] = None,
    ) -> RestResponse:
        if file_paths:
            for file_path in file_paths:
                with open(file_path, "rb") as file:
                    return self._exec_request(
                        url=url,
                        method=method,
                        headers=headers,
                        params=params,
                        body=body,
                        files=[("file", (file_path, file))],
                    )

        else:
            return self._exec_request(
                url=url,
                method=method,
                headers=headers,
                params=params,
                body=body,
            )
