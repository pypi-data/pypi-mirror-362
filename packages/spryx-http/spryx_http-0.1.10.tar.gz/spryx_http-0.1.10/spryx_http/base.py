import time
from typing import (
    Any,
    Dict,
    List,
    NotRequired,
    Optional,
    Type,
    TypedDict,
    TypeVar,
    Union,
)

import httpx
import logfire
from pydantic import BaseModel
from spryx_core.time import timestamp_from_iso

from spryx_http.auth import AuthStrategy, NoAuth
from spryx_http.exceptions import raise_for_status
from spryx_http.retry import build_retry_transport
from spryx_http.settings import HttpClientSettings, get_http_settings

T = TypeVar("T", bound=BaseModel)


# Define the TypedDict for request parameters
class RequestKwargs(TypedDict):
    method: str
    url: str
    params: NotRequired[Optional[Dict[str, Any]]]
    json: NotRequired[Optional[Dict[str, Any]]]
    headers: NotRequired[Dict[str, str]]
    # Add other common httpx request parameters
    timeout: NotRequired[Optional[Union[float, httpx.Timeout]]]
    follow_redirects: NotRequired[Optional[bool]]
    content: NotRequired[Optional[Any]]


class SpryxClientBase:
    """Base class for Spryx HTTP clients with common functionality.

    Contains shared functionality between async and sync clients:
    - Token management and validation
    - Authentication configuration
    - Response data processing
    - Settings management
    """

    _token: Optional[str] = None
    _token_expires_at: Optional[int] = None
    _refresh_token: Optional[str] = None
    _refresh_token_expires_at: Optional[int] = None

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        application_id: Optional[str] = None,
        application_secret: Optional[str] = None,
        auth_strategy: Optional[AuthStrategy] = None,
        settings: Optional[HttpClientSettings] = None,
        iam_base_url: Optional[str] = None,
        **kwargs,
    ):
        """Initialize the base Spryx HTTP client.

        Args:
            base_url: Base URL for all API requests. Can be None.
            application_id: Application ID for authentication.
            application_secret: Application secret for authentication.
            auth_strategy: Authentication strategy to use.
            settings: HTTP client settings.
            iam_base_url: IAM base URL for authentication.
            **kwargs: Additional arguments to pass to httpx client.
        """
        self._base_url = base_url
        self._iam_base_url = iam_base_url

        self._application_id = application_id
        self._application_secret = application_secret

        self.auth_strategy = auth_strategy or NoAuth()
        self.settings = settings or get_http_settings()

        # Configure timeout if not provided
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.settings.timeout_s

        self._token_expires_at = None
        self._httpx_kwargs = kwargs

    def _get_transport_kwargs(self, **kwargs):
        """Get transport configuration for the client.

        This method should be overridden by subclasses to provide
        the appropriate transport configuration.
        """
        # Configure retry transport if not provided
        if "transport" not in kwargs:
            kwargs["transport"] = build_retry_transport(
                settings=self.settings, is_async=True
            )
        return kwargs

    @property
    def is_token_expired(self) -> bool:
        """Check if the access token is expired.

        Returns:
            bool: True if the token is expired or not set, False otherwise.
        """
        if self._token is None or self._token_expires_at is None:
            return True

        current_time = int(time.time())
        return current_time >= self._token_expires_at

    @property
    def is_refresh_token_expired(self) -> bool:
        """Check if the refresh token is expired.

        Returns:
            bool: True if the refresh token is expired or not set, False otherwise.
        """
        if self._refresh_token is None or self._refresh_token_expires_at is None:
            return True

        current_time = int(time.time())
        return current_time >= self._refresh_token_expires_at

    def _extract_data_from_response(self, response_data: Dict[str, Any]) -> Any:
        """Extract data from standardized API response.

        In our standardized API response, the actual entity is always under a 'data' key.

        Args:
            response_data: The response data dictionary.

        Returns:
            Any: The extracted data.
        """
        if "data" in response_data:
            return response_data["data"]
        return response_data

    def _parse_model_data(self, model_cls: Type[T], data: Any) -> Union[T, List[T]]:
        """Parse data into a Pydantic model or list of models.

        Args:
            model_cls: The Pydantic model class to parse into.
            data: The data to parse.

        Returns:
            Union[T, List[T]]: Parsed model instance(s).
        """
        if isinstance(data, list):
            return [model_cls.model_validate(item) for item in data]
        return model_cls.model_validate(data)

    def _process_response_data(
        self, response: httpx.Response, cast_to: Optional[Type[T]] = None
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Process the response by validating status and converting to model.

        Args:
            response: The HTTP response.
            cast_to: Optional Pydantic model class to parse response into.
                     If None, returns the raw JSON data.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        # Raise exception for error status codes
        raise_for_status(response)

        # Parse JSON response
        try:
            json_data = response.json()
        except ValueError:
            raise ValueError(f"Failed to parse JSON response: {response.text}")

        # Extract data from standard response format
        data = self._extract_data_from_response(json_data)

        # If cast_to is provided, parse into model, otherwise return the raw data
        if cast_to is not None:
            return self._parse_model_data(cast_to, data)
        return data


class SpryxAsyncClient(SpryxClientBase, httpx.AsyncClient):
    """Spryx HTTP async client with retry, tracing, and auth capabilities.

    Extends httpx.AsyncClient with:
    - Retry with exponential backoff
    - Authentication via pluggable strategies
    - Structured logging with Logfire
    - Correlation ID propagation
    - Pydantic model response parsing
    """

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        application_id: Optional[str] = None,
        application_secret: Optional[str] = None,
        auth_strategy: Optional[AuthStrategy] = None,
        settings: Optional[HttpClientSettings] = None,
        iam_base_url: Optional[str] = None,
        **kwargs,
    ):
        """Initialize the Spryx HTTP async client.

        Args:
            base_url: Base URL for all API requests. Can be None.
            application_id: Application ID for authentication.
            application_secret: Application secret for authentication.
            auth_strategy: Authentication strategy to use.
            settings: HTTP client settings.
            iam_base_url: IAM base URL for authentication.
            **kwargs: Additional arguments to pass to httpx.AsyncClient.
        """
        # Initialize base class
        SpryxClientBase.__init__(
            self,
            base_url=base_url,
            application_id=application_id,
            application_secret=application_secret,
            auth_strategy=auth_strategy,
            settings=settings,
            iam_base_url=iam_base_url,
            **kwargs,
        )

        # Initialize httpx.AsyncClient with async transport
        transport_kwargs = self._get_transport_kwargs(**self._httpx_kwargs)
        # Pass empty string instead of None to httpx.AsyncClient
        httpx_base_url = "" if self._base_url is None else self._base_url
        httpx.AsyncClient.__init__(self, base_url=httpx_base_url, **transport_kwargs)

    async def authenticate_application(self) -> str:
        """Authenticate the application with credentials provided in the constructor.

        Uses the application_id and application_secret provided during initialization
        to authenticate with the API and obtain access and refresh tokens.

        Raises:
            ValueError: If application_id or application_secret is not provided.
        """
        if self._application_id is None:
            raise ValueError("application_id is required")

        if self._application_secret is None:
            raise ValueError("application_secret is required")

        payload = {
            "application_id": self._application_id,
            "application_secret": self._application_secret,
        }
        response = await self.request(
            "POST", f"{self._iam_base_url}/v1/auth/application", json=payload
        )
        json_response = response.json()
        data = json_response.get("data", {})

        self._token_expires_at = timestamp_from_iso(data.get("data", {}).get("exp"))
        self._token = data.get("access_token")
        self._refresh_token = data.get("refresh_token")
        return self._token

    async def _generate_new_token(self):
        """Generate a new access token using the refresh token.

        This method is called automatically when the access token expires
        but the refresh token is still valid.

        Raises:
            ValueError: If refresh token is not available.
        """
        if self._refresh_token is None:
            raise ValueError(
                "Refresh token is not available. Please authenticate with authenticate_application() first."
            )

        try:
            payload = {"refresh_token": self._refresh_token}

            response = await self.request(
                "POST",
                url=f"{self._iam_base_url}/v1/auth/refresh-token",
                json=payload,
            )

            response.raise_for_status()

            json_response = response.json()
            data = json_response.get("data")

            self._token_expires_at = timestamp_from_iso(data.get("exp"))
            self._token = json_response.get("access_token")
        except (httpx.RequestError, httpx.HTTPStatusError, ValueError, KeyError):
            return await self.authenticate_application()

    async def _get_token(self) -> str:
        """Get a valid authentication token.

        This method handles token lifecycle management, including:
        - Initial authentication if no token exists
        - Re-authentication if refresh token has expired
        - Token refresh if access token has expired but refresh token is valid

        Returns:
            str: A valid authentication token.

        Raises:
            Exception: If unable to obtain a valid token.
        """
        if self._token is None:
            await self.authenticate_application()
            if self._token is None:
                raise Exception(
                    "Failed to obtain a valid authentication token. Authentication did not provide a token."
                )

        if self.is_token_expired:
            await self._generate_new_token()
            if self._token is None:
                raise Exception(
                    "Failed to obtain a valid authentication token. Token refresh did not provide a token."
                )

        # At this point, we've done all we can to get a valid token
        # If it's still None, raise an exception
        if self._token is None:
            raise Exception(
                "Failed to obtain a valid authentication token. Check your credentials and try again."
            )

        return self._token

    async def request(
        self,
        method: str,
        url: Union[str, httpx.URL],
        *,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> httpx.Response:
        """Send an HTTP request with added functionality.

        Extends the base request method with:
        - Adding authentication headers
        - Adding correlation ID
        - Structured logging

        Args:
            method: HTTP method.
            url: Request URL.
            headers: Request headers.
            **kwargs: Additional arguments to pass to the base request method.

        Returns:
            httpx.Response: The HTTP response.
        """
        # Initialize headers if None
        headers = headers or {}

        # Add authentication headers
        auth_headers = self.auth_strategy.headers()
        headers.update(auth_headers)

        # Log the request with Logfire
        logfire.debug(
            "HTTP request",
            http_method=method,
            url=str(url),
        )

        try:
            response = await super().request(method, url, headers=headers, **kwargs)

            # Log the response with Logfire
            logfire.debug(
                "HTTP response",
                status_code=response.status_code,
                url=str(url),
            )

            return response
        except httpx.RequestError as e:
            # Log the error with Logfire
            logfire.error(
                "HTTP request error",
                error=str(e),
                url=str(url),
                _exc_info=True,
            )
            raise

    async def _handle_authentication(
        self, response: httpx.Response, **request_kwargs: RequestKwargs
    ) -> httpx.Response:
        """Handle authentication failures by refreshing token and retrying."""
        if response.status_code != 401:
            return response

        await self.authenticate_application()
        if self._token is None:
            raise Exception(
                "Failed to obtain a valid authentication token. Authentication did not provide a token."
            )

        # Retry the request with the new token
        headers = request_kwargs.get("headers", {})
        headers.update({"Authorization": f"Bearer {self._token}"})
        request_kwargs["headers"] = headers

        return await self.request(**request_kwargs)

    async def _process_response(
        self, response: httpx.Response, cast_to: Optional[Type[T]] = None
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Process the response by validating status and converting to model.

        Args:
            response: The HTTP response.
            cast_to: Optional Pydantic model class to parse response into.
                     If None, returns the raw JSON data.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        return self._process_response_data(response, cast_to)

    async def _make_request(
        self,
        method: str,
        path: str,
        *,
        cast_to: Optional[Type[T]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Core request method to handle HTTP requests with optional Pydantic model parsing.

        Args:
            method: HTTP method.
            path: Request path to be appended to base_url or a full URL if base_url is None.
            cast_to: Optional Pydantic model class to parse response into.
                    If None, returns the raw JSON data.
            params: Optional query parameters.
            json: Optional JSON data for the request body.
            headers: Optional request headers.
            **kwargs: Additional arguments to pass to the request method.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        # Check if path is a full URL when base_url is None
        if self._base_url is None and not path.startswith(("http://", "https://")):
            raise ValueError(
                "Either base_url must be provided during initialization or path must be a full URL"
            )

        # Handle path to prevent double slashes if it's not a full URL
        if not path.startswith(("http://", "https://")):
            path = path.lstrip("/")

        # Get authentication token
        token = await self._get_token()

        # Create RequestKwargs with required fields
        request_kwargs: RequestKwargs = {
            "method": method,
            "url": path,
        }

        # Add optional parameters if provided
        if params is not None:
            request_kwargs["params"] = params

        if json is not None:
            request_kwargs["json"] = json

        # Handle headers
        request_headers = headers or {}
        request_headers.update({"Authorization": f"Bearer {token}"})
        request_kwargs["headers"] = request_headers

        # Add any additional kwargs
        for key, value in kwargs.items():
            request_kwargs[key] = value

        # Make the request
        try:
            response = await self.request(**request_kwargs)
        except httpx.UnsupportedProtocol:
            raise ValueError(
                "Either base_url must be provided during initialization or path must be a full URL"
            )

        # Handle authentication failures
        if response.status_code == 401:
            response = await self._handle_authentication(response, **request_kwargs)

        # Process the response
        return await self._process_response(response, cast_to)

    async def get(
        self,
        path: str,
        *,
        cast_to: Optional[Type[T]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Send a GET request.

        Args:
            path: Request path to be appended to base_url.
            cast_to: Optional Pydantic model class to parse response into.
                    If None, returns the raw JSON data.
            params: Optional query parameters.
            **kwargs: Additional arguments to pass to the request method.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        return await self._make_request(
            "GET", path, cast_to=cast_to, params=params, **kwargs
        )

    async def post(
        self,
        path: str,
        *,
        cast_to: Optional[Type[T]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Send a POST request.

        Args:
            path: Request path to be appended to base_url.
            cast_to: Optional Pydantic model class to parse response into.
                    If None, returns the raw JSON data.
            json: Optional JSON data for the request body.
            **kwargs: Additional arguments to pass to the request method.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        return await self._make_request(
            "POST", path, cast_to=cast_to, json=json, **kwargs
        )

    async def put(
        self,
        path: str,
        *,
        cast_to: Optional[Type[T]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Send a PUT request.

        Args:
            path: Request path to be appended to base_url.
            cast_to: Optional Pydantic model class to parse response into.
                    If None, returns the raw JSON data.
            json: Optional JSON data for the request body.
            **kwargs: Additional arguments to pass to the request method.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        return await self._make_request(
            "PUT", path, cast_to=cast_to, json=json, **kwargs
        )

    async def patch(
        self,
        path: str,
        *,
        cast_to: Optional[Type[T]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Send a PATCH request.

        Args:
            path: Request path to be appended to base_url.
            cast_to: Optional Pydantic model class to parse response into.
                    If None, returns the raw JSON data.
            json: Optional JSON data for the request body.
            **kwargs: Additional arguments to pass to the request method.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        return await self._make_request(
            "PATCH", path, cast_to=cast_to, json=json, **kwargs
        )

    async def delete(
        self,
        path: str,
        *,
        cast_to: Optional[Type[T]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Send a DELETE request.

        Args:
            path: Request path to be appended to base_url.
            cast_to: Optional Pydantic model class to parse response into.
                    If None, returns the raw JSON data.
            params: Optional query parameters.
            **kwargs: Additional arguments to pass to the request method.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        return await self._make_request(
            "DELETE", path, cast_to=cast_to, params=params, **kwargs
        )


class SpryxSyncClient(SpryxClientBase, httpx.Client):
    """Spryx HTTP synchronous client with retry, tracing, and auth capabilities.

    Extends httpx.Client with:
    - Retry with exponential backoff
    - Authentication via pluggable strategies
    - Structured logging with Logfire
    - Correlation ID propagation
    - Pydantic model response parsing
    """

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        application_id: Optional[str] = None,
        application_secret: Optional[str] = None,
        auth_strategy: Optional[AuthStrategy] = None,
        settings: Optional[HttpClientSettings] = None,
        iam_base_url: Optional[str] = None,
        **kwargs,
    ):
        """Initialize the Spryx HTTP sync client.

        Args:
            base_url: Base URL for all API requests. Can be None.
            application_id: Application ID for authentication.
            application_secret: Application secret for authentication.
            auth_strategy: Authentication strategy to use.
            settings: HTTP client settings.
            iam_base_url: IAM base URL for authentication.
            **kwargs: Additional arguments to pass to httpx.Client.
        """
        # Initialize base class
        SpryxClientBase.__init__(
            self,
            base_url=base_url,
            application_id=application_id,
            application_secret=application_secret,
            auth_strategy=auth_strategy,
            settings=settings,
            iam_base_url=iam_base_url,
            **kwargs,
        )

        # Initialize httpx.Client with sync transport
        transport_kwargs = self._get_sync_transport_kwargs(**self._httpx_kwargs)
        # Pass empty string instead of None to httpx.Client
        httpx_base_url = "" if self._base_url is None else self._base_url
        httpx.Client.__init__(self, base_url=httpx_base_url, **transport_kwargs)

    def _get_sync_transport_kwargs(self, **kwargs):
        """Get sync transport configuration for the client."""
        # Configure retry transport if not provided
        if "transport" not in kwargs:
            kwargs["transport"] = build_retry_transport(
                settings=self.settings, is_async=False
            )
        return kwargs

    def authenticate_application(self) -> str:
        """Authenticate the application with credentials provided in the constructor.

        Uses the application_id and application_secret provided during initialization
        to authenticate with the API and obtain access and refresh tokens.

        Raises:
            ValueError: If application_id or application_secret is not provided.
        """
        if self._application_id is None:
            raise ValueError("application_id is required")

        if self._application_secret is None:
            raise ValueError("application_secret is required")

        payload = {
            "application_id": self._application_id,
            "application_secret": self._application_secret,
        }
        response = self.request(
            "POST", f"{self._iam_base_url}/v1/auth/application", json=payload
        )
        json_response = response.json()
        data = json_response.get("data", {})

        self._token_expires_at = timestamp_from_iso(data.get("data", {}).get("exp"))
        self._token = data.get("access_token")
        self._refresh_token = data.get("refresh_token")
        return self._token

    def _generate_new_token(self):
        """Generate a new access token using the refresh token.

        This method is called automatically when the access token expires
        but the refresh token is still valid.

        Raises:
            ValueError: If refresh token is not available.
        """
        if self._refresh_token is None:
            raise ValueError(
                "Refresh token is not available. Please authenticate with authenticate_application() first."
            )

        try:
            payload = {"refresh_token": self._refresh_token}

            response = self.request(
                "POST",
                url=f"{self._iam_base_url}/v1/auth/refresh-token",
                json=payload,
            )

            response.raise_for_status()

            json_response = response.json()
            data = json_response.get("data")

            self._token_expires_at = timestamp_from_iso(data.get("exp"))
            self._token = json_response.get("access_token")
        except (httpx.RequestError, httpx.HTTPStatusError, ValueError, KeyError):
            return self.authenticate_application()

    def _get_token(self) -> str:
        """Get a valid authentication token.

        This method handles token lifecycle management, including:
        - Initial authentication if no token exists
        - Re-authentication if refresh token has expired
        - Token refresh if access token has expired but refresh token is valid

        Returns:
            str: A valid authentication token.

        Raises:
            Exception: If unable to obtain a valid token.
        """
        if self._token is None:
            self.authenticate_application()
            if self._token is None:
                raise Exception(
                    "Failed to obtain a valid authentication token. Authentication did not provide a token."
                )

        if self.is_token_expired:
            self._generate_new_token()
            if self._token is None:
                raise Exception(
                    "Failed to obtain a valid authentication token. Token refresh did not provide a token."
                )

        # At this point, we've done all we can to get a valid token
        # If it's still None, raise an exception
        if self._token is None:
            raise Exception(
                "Failed to obtain a valid authentication token. Check your credentials and try again."
            )

        return self._token

    def request(
        self,
        method: str,
        url: Union[str, httpx.URL],
        *,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> httpx.Response:
        """Send an HTTP request with added functionality.

        Extends the base request method with:
        - Adding authentication headers
        - Adding correlation ID
        - Structured logging

        Args:
            method: HTTP method.
            url: Request URL.
            headers: Request headers.
            **kwargs: Additional arguments to pass to the base request method.

        Returns:
            httpx.Response: The HTTP response.
        """
        # Initialize headers if None
        headers = headers or {}

        # Add authentication headers
        auth_headers = self.auth_strategy.headers()
        headers.update(auth_headers)

        # Log the request with Logfire
        logfire.debug(
            "HTTP request",
            http_method=method,
            url=str(url),
        )

        try:
            response = super().request(method, url, headers=headers, **kwargs)

            # Log the response with Logfire
            logfire.debug(
                "HTTP response",
                status_code=response.status_code,
                url=str(url),
            )

            return response
        except httpx.RequestError as e:
            # Log the error with Logfire
            logfire.error(
                "HTTP request error",
                error=str(e),
                url=str(url),
                _exc_info=True,
            )
            raise

    def _handle_authentication(
        self, response: httpx.Response, **request_kwargs: RequestKwargs
    ) -> httpx.Response:
        """Handle authentication failures by refreshing token and retrying."""
        if response.status_code != 401:
            return response

        self.authenticate_application()
        if self._token is None:
            raise Exception(
                "Failed to obtain a valid authentication token. Authentication did not provide a token."
            )

        # Retry the request with the new token
        headers = request_kwargs.get("headers", {})
        headers.update({"Authorization": f"Bearer {self._token}"})
        request_kwargs["headers"] = headers

        return self.request(**request_kwargs)

    def _process_response(
        self, response: httpx.Response, cast_to: Optional[Type[T]] = None
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Process the response by validating status and converting to model.

        Args:
            response: The HTTP response.
            cast_to: Optional Pydantic model class to parse response into.
                     If None, returns the raw JSON data.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        return self._process_response_data(response, cast_to)

    def _make_request(
        self,
        method: str,
        path: str,
        *,
        cast_to: Optional[Type[T]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Core request method to handle HTTP requests with optional Pydantic model parsing.

        Args:
            method: HTTP method.
            path: Request path to be appended to base_url or a full URL if base_url is None.
            cast_to: Optional Pydantic model class to parse response into.
                    If None, returns the raw JSON data.
            params: Optional query parameters.
            json: Optional JSON data for the request body.
            headers: Optional request headers.
            **kwargs: Additional arguments to pass to the request method.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        # Check if path is a full URL when base_url is None
        if self._base_url is None and not path.startswith(("http://", "https://")):
            raise ValueError(
                "Either base_url must be provided during initialization or path must be a full URL"
            )

        # Handle path to prevent double slashes if it's not a full URL
        if not path.startswith(("http://", "https://")):
            path = path.lstrip("/")

        # Get authentication token
        token = self._get_token()

        # Create RequestKwargs with required fields
        request_kwargs: RequestKwargs = {
            "method": method,
            "url": path,
        }

        # Add optional parameters if provided
        if params is not None:
            request_kwargs["params"] = params

        if json is not None:
            request_kwargs["json"] = json

        # Handle headers
        request_headers = headers or {}
        request_headers.update({"Authorization": f"Bearer {token}"})
        request_kwargs["headers"] = request_headers

        # Add any additional kwargs
        for key, value in kwargs.items():
            request_kwargs[key] = value

        # Make the request
        try:
            response = self.request(**request_kwargs)
        except httpx.UnsupportedProtocol:
            raise ValueError(
                "Either base_url must be provided during initialization or path must be a full URL"
            )

        # Handle authentication failures
        if response.status_code == 401:
            response = self._handle_authentication(response, **request_kwargs)

        # Process the response
        return self._process_response(response, cast_to)

    def get(
        self,
        path: str,
        *,
        cast_to: Optional[Type[T]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Send a GET request.

        Args:
            path: Request path to be appended to base_url.
            cast_to: Optional Pydantic model class to parse response into.
                    If None, returns the raw JSON data.
            params: Optional query parameters.
            **kwargs: Additional arguments to pass to the request method.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        return self._make_request("GET", path, cast_to=cast_to, params=params, **kwargs)

    def post(
        self,
        path: str,
        *,
        cast_to: Optional[Type[T]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Send a POST request.

        Args:
            path: Request path to be appended to base_url.
            cast_to: Optional Pydantic model class to parse response into.
                    If None, returns the raw JSON data.
            json: Optional JSON data for the request body.
            **kwargs: Additional arguments to pass to the request method.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        return self._make_request("POST", path, cast_to=cast_to, json=json, **kwargs)

    def put(
        self,
        path: str,
        *,
        cast_to: Optional[Type[T]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Send a PUT request.

        Args:
            path: Request path to be appended to base_url.
            cast_to: Optional Pydantic model class to parse response into.
                    If None, returns the raw JSON data.
            json: Optional JSON data for the request body.
            **kwargs: Additional arguments to pass to the request method.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        return self._make_request("PUT", path, cast_to=cast_to, json=json, **kwargs)

    def patch(
        self,
        path: str,
        *,
        cast_to: Optional[Type[T]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Send a PATCH request.

        Args:
            path: Request path to be appended to base_url.
            cast_to: Optional Pydantic model class to parse response into.
                    If None, returns the raw JSON data.
            json: Optional JSON data for the request body.
            **kwargs: Additional arguments to pass to the request method.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        return self._make_request("PATCH", path, cast_to=cast_to, json=json, **kwargs)

    def delete(
        self,
        path: str,
        *,
        cast_to: Optional[Type[T]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
        """Send a DELETE request.

        Args:
            path: Request path to be appended to base_url.
            cast_to: Optional Pydantic model class to parse response into.
                    If None, returns the raw JSON data.
            params: Optional query parameters.
            **kwargs: Additional arguments to pass to the request method.

        Returns:
            Union[T, List[T], Dict[str, Any], List[Dict[str, Any]]]:
                Pydantic model instance(s) or raw JSON data.
        """
        return self._make_request(
            "DELETE", path, cast_to=cast_to, params=params, **kwargs
        )
