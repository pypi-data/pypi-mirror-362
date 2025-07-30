"""
Main client module for the PRC API Wrapper.
"""

import time
import logging
from typing import Optional, Any, Dict, Union
import requests
from requests import Response, Session
from .exceptions import PRCError, PRCRateLimitError, PRCConnectionError, PRCAuthenticationError, PRCServerError
from .models import PRCResponse, ErrorCode
from .utils import validate_server_key

_LOGGER = logging.getLogger(__name__)

class PRCClient:
    BASE_URL = "https://api.policeroleplay.community/v1"

    def __init__(
        self,
        server_key: str,
        global_api_key: Optional[str] = None,
        rate_limit_delay: float = 1.0,
        auto_retry: bool = True,
        max_retries: int = 3,
        timeout: int = 30,
        raise_on_error: bool = False,
    ):
        """
        Initialize the PRC API client.

        Args:
            server_key (str): Server key to authenticate requests.
            global_api_key (Optional[str]): Optional global API key for higher rate limits.
            rate_limit_delay (float): Delay between requests to respect rate limits.
            auto_retry (bool): Whether to automatically retry on rate limit errors.
            max_retries (int): Max number of retry attempts on rate limiting.
            timeout (int): Request timeout in seconds.
            raise_on_error (bool): Raise exceptions on API errors if True.
        """
        if not validate_server_key(server_key):
            raise ValueError("Invalid or empty server key provided.")

        self.server_key = server_key
        self.global_api_key = global_api_key
        self.rate_limit_delay = rate_limit_delay
        self.auto_retry = auto_retry
        self.max_retries = max_retries
        self.timeout = timeout
        self.raise_on_error = raise_on_error

        self.session: Session = requests.Session()
        self.session.headers.update({
            "User-Agent": "prc-api-wrapper/1.0",
            "Accept": "application/json",
        })

        self._last_request_time = 0.0

    def _wait_rate_limit(self):
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)

    def _build_headers(self) -> Dict[str, str]:
        headers = {
            "Server-Key": self.server_key,
        }
        if self.global_api_key:
            headers["Global-API-Key"] = self.global_api_key
        return headers

    def _handle_response(self, response: Response) -> PRCResponse:
        self._last_request_time = time.time()

        if response.status_code == 429:
            raise PRCRateLimitError(PRCResponse(
                success=False,
                status_code=response.status_code,
                error_code=ErrorCode.RATE_LIMITED,
                error_message="Rate limit exceeded",
                raw_response=response.json() if response.content else None,
            ))

        if response.status_code >= 500:
            raise PRCServerError(PRCResponse(
                success=False,
                status_code=response.status_code,
                error_code=ErrorCode.INTERNAL_ERROR,
                error_message=f"Server error {response.status_code}",
                raw_response=response.json() if response.content else None,
            ))

        try:
            data = response.json()
        except Exception as e:
            raise PRCConnectionError(PRCResponse(
                success=False,
                status_code=response.status_code,
                error_message=f"Failed to parse JSON response: {str(e)}",
                raw_response=None,
            ))

        # If error_code present, treat as failure
        error_code = ErrorCode(data.get("error_code", 0))
        success = response.status_code == 200 and error_code == ErrorCode.UNKNOWN
        error_message = data.get("error_message") or data.get("error") or None

        prc_response = PRCResponse(
            success=success,
            status_code=response.status_code,
            data=data if success else None,
            error_code=error_code if not success else None,
            error_message=error_message,
            raw_response=data,
        )

        if not success and self.raise_on_error:
            if error_code == ErrorCode.RATE_LIMITED:
                raise PRCRateLimitError(prc_response)
            elif error_code in (ErrorCode.NO_SERVER_KEY, ErrorCode.INVALID_SERVER_KEY, ErrorCode.INVALID_SERVER_KEY_FORMAT):
                raise PRCAuthenticationError(prc_response)
            else:
                raise PRCError(prc_response)

        return prc_response

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> PRCResponse:
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        headers = self._build_headers()

        for attempt in range(1, self.max_retries + 2):  # retries + first try
            self._wait_rate_limit()
            try:
                response = self.session.request(
                    method=method.upper(),
                    url=url,
                    headers=headers,
                    params=params,
                    json=data,
                    timeout=self.timeout,
                )
                prc_response = self._handle_response(response)
                return prc_response

            except PRCRateLimitError as e:
                if not self.auto_retry or attempt > self.max_retries:
                    raise
                else:
                    _LOGGER.warning(f"Rate limited, retrying attempt {attempt}/{self.max_retries}...")
                    time.sleep(self.rate_limit_delay * attempt)

            except requests.RequestException as e:
                raise PRCConnectionError(PRCResponse(
                    success=False,
                    status_code=0,
                    error_message=f"Request failed: {str(e)}",
                    raw_response=None,
                ))

        # If somehow we exit loop without return:
        return PRCResponse(success=False, status_code=0, error_message="Request failed after retries.")

    def get_server_status(self) -> PRCResponse:
        """
        Get the server status information.
        """
        return self._request("GET", "server/status")

    def get_players(self) -> PRCResponse:
        """
        Get the list of current players.
        """
        return self._request("GET", "server/players")

    def get_join_logs(self) -> PRCResponse:
        """
        Get join/leave logs.
        """
        return self._request("GET", "server/joinlogs")

    def get_queue(self) -> PRCResponse:
        """
        Get the player queue.
        """
        return self._request("GET", "server/queue")

    def get_kill_logs(self) -> PRCResponse:
        """
        Get kill logs.
        """
        return self._request("GET", "server/killlogs")

    def get_command_logs(self) -> PRCResponse:
        """
        Get command logs.
        """
        return self._request("GET", "server/commandlogs")

    def get_mod_calls(self) -> PRCResponse:
        """
        Get moderator calls.
        """
        return self._request("GET", "server/modcalls")

    def get_bans(self) -> PRCResponse:
        """
        Get banned players.
        """
        return self._request("GET", "server/bans")

    def get_vehicles(self) -> PRCResponse:
        """
        Get spawned vehicles.
        """
        return self._request("GET", "server/vehicles")

    def run_command(self, command: str) -> PRCResponse:
        """
        Run a server command.

        Args:
            command (str): The command string to run.

        Returns:
            PRCResponse: The API response.
        """
        if not command or not isinstance(command, str):
            raise ValueError("Command must be a non-empty string.")

        return self._request("POST", "server/command", data={"command": command})

    def close(self) -> None:
        """
        Close the client session.
        """
        self.session.close()

    def __enter__(self) -> "PRCClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
