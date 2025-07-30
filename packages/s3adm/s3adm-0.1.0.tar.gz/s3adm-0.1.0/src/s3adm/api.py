import sys
import httpx
from typing import Optional
from httpx_auth import AWS4Auth
import logging

_logger = logging.getLogger(__name__)

class CephAdminApi():
    """ Class for ceph admin api interactions. """

    _client: Optional[httpx.Client] = None

    def __init__(self,
                schema: str,
                host: str,
                port: int,
                access_key: str,
                secret_key: str,
                insecure: bool = True,
                timeout: int = 30 ) -> None:
        if access_key is None:
            _logger.critical("Access key must be provided.")
            sys.exit(1)
        if secret_key is None:
            _logger.critical("Secret key must be provided.")
            sys.exit(1)
        self._auth = AWS4Auth(
            access_id=access_key,
            secret_key=secret_key,
            region="default",
            service="s3"
        )
        self._insecure = insecure
        self._api_url = f"{schema}://{host}:{port}/admin"
        self._timeout = timeout

    def __enter__(self) -> "CephAdminApi":
        """ Enter the context manager, returning the API instance. """
        if self._client is None:
            self._client = self._connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """ Exit the context manager, closing the HTTP client if it exists. """
        if self._client:
            self._client.close()
            _logger.debug("HTTP client closed.")

    def _connect(self) -> httpx.Client:
        """ Create a new HTTP client for API requests. """
        verify = not self._insecure
        client = httpx.Client(
            base_url=self._api_url,
            verify=verify,
            auth=self._auth,
            timeout=httpx.Timeout(self._timeout)
        )
        _logger.debug("HTTP client created with base URL: %s", self._api_url)
        return client

    def request(self, request: str, params: Optional[str] = None) -> httpx.Response:
        """ Get information about the Ceph cluster. """
        if params:
            request += f"?{params}"
        try:
            if self._client is None:
                self._client = self._connect()
            response: httpx.Response = self._client.get("/" + request)
            response.raise_for_status()
            _logger.debug("Ceph cluster info: %s", response.json())
        except httpx.HTTPStatusError as e:
            _logger.error("Failed to get Ceph cluster info: %s", e)
            sys.exit(1)
        except httpx.RequestError as e:
            _logger.error("Request error: %s", e)
            sys.exit(1)
        return response