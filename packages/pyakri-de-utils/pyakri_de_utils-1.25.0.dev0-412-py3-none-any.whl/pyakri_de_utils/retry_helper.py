from urllib3 import Retry


def get_http_retry(
    total=6,
    backoff_factor=1,
    status_forcelist=frozenset(range(500, 600)),
    allowed_methods=frozenset(
        ["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST", "PATCH"]
    ),
) -> Retry:
    """
    get_http_retry returns a Retry object which retries on 5XX status code
    for "HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST", "PATCH"
    """
    return Retry(
        total=total,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=allowed_methods,
    )
