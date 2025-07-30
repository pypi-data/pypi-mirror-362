from typing import Any

from pyakri_de_utils import logger
from pyakri_de_utils.rest.exceptions import RestClientException
from pyakri_de_utils.rest.rest_client import RestClient
from pyakri_de_utils.rest.models import RestResponse
from pyakri_de_utils.rest.utils import default_rest_client


def upload_file_to_data_store(
    file_path: str,
    presigned_url: str,
    fields: Any,
    rest_client: RestClient = default_rest_client(),
):
    logger.debug(
        f"Uploading file {file_path} to datastore, pre-signed url "
        f"{presigned_url} with fields {fields}"
    )
    try:
        response: RestResponse = rest_client.exec_post_request(
            url=presigned_url, body=fields, file_paths=[file_path]
        )
        logger.debug(f"Upload response: {response}")
    except RestClientException:
        logger.exception(f"Failed to upload file")
        raise
