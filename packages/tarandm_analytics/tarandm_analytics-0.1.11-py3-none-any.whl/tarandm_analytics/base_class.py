from typing import Optional

import requests
import structlog
from requests.auth import HTTPBasicAuth

logger = structlog.get_logger(__name__)


class TaranDMAnalytics:
    def __init__(
        self,
        endpoint_url: Optional[str],
        username: Optional[str],
        password: Optional[str],
        skip_endpoint_validation: bool = False,
    ) -> None:
        if endpoint_url is not None:
            self.endpoint_url = endpoint_url + ("" if endpoint_url.endswith("/") else "/")
        self.username = username
        self.password = password

        # endpoint validation might be skipped if only methods that do not use endpoint are to be used
        if not skip_endpoint_validation:
            self.validate_url()

    def validate_url(self) -> None:
        url = self.endpoint_url + "info"
        response = requests.get(url=url, auth=HTTPBasicAuth(self.username, self.password))

        if response.status_code == 200:
            logger.info(f"Connection to {self.endpoint_url} was established.")
        elif response.status_code == 401:
            logger.info(
                f"Connection to {self.endpoint_url} cannot be established. Endpoint error message: " f"{response.text}"
            )
