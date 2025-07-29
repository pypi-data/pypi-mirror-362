from logging import getLogger
from urllib.parse import urljoin

from requests import RequestException, Response, Session

logger = getLogger(__name__)


class Requester:
    """
    An instance of this class communicates with service Mulesoft API.
    """

    def __init__(
        self, base_url: str | None = None, token: str | None = None, **kwargs
    ) -> None:
        """
        Create a edm_client instance with the provided options.

        :param base_url: string
        :param token: token for making api calls
        :param timeout: requests timeout
        :param raise_request_exc: re-raise RequestException(s) after logging them
        """
        self.base_url = base_url or ""
        self.__token = token
        self._session = Session()
        if token is not None:
            self._session.headers.update({"Authorization": f"Bearer {token}"})
        self.__kwargs = kwargs

    def send(
        self,
        method: str,
        endpoint: str | None = None,
        params: dict | None = None,
        payload: str | None = None,
        headers: dict | None = None,
        **kwargs,
    ) -> Response | None:
        """
        Helper function to call the API

        :param endpoint: URL to the service
        :param method: HTTP verb
        :param payload: payload for the request
        :param headers: request headers
        :param timeout: request timeout
        :param raise_request_exc: re-raise RequestException(s) after logging them
        :return: API response
        """
        kwargs = {**self.__kwargs, **kwargs}
        timeout = kwargs.get("timeout")

        if endpoint:
            if not self.base_url.endswith("/"):
                base_url = self.base_url + "/"
            url = urljoin(base_url, endpoint)
        else:
            url = self.base_url

        try:
            return self._session.request(
                method=method,
                url=url,
                params=params,
                data=payload,
                headers=headers,
                timeout=timeout,
            )
        except RequestException as e:
            logger.error(str(e))
            if kwargs.get("raise_request_exc"):
                raise

    def get(
        self,
        endpoint: str | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        **kwargs,
    ) -> Response | None:
        """Shortcut for invoking send() with method GET"""
        return self.send(
            method="GET", endpoint=endpoint, params=params, headers=headers, **kwargs
        )

    @property
    def token(self) -> str | None:
        return self.__token

    @token.setter
    def token(self, token: str) -> None:
        """
        Set the token for the request
        """
        logger.debug("Updating token in requester")
        self.__token = token
        self._session.headers.update({"Authorization": f"Bearer {token}"})
