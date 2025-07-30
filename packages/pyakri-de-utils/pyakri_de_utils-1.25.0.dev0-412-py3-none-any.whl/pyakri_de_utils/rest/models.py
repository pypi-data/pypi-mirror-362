from typing import Optional
from dataclasses import dataclass


@dataclass
class RestResponse:
    status_code: int
    json_data: Optional[dict]
    message: str
