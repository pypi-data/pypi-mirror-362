from pyakri_de_utils.rest.rest_client import RestClient
from pyakri_de_utils.retry_helper import get_http_retry


def default_rest_client():
    return RestClient.get_client(retry=get_http_retry())
