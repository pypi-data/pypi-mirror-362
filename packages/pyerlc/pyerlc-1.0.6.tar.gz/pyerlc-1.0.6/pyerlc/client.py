import requests
from typing import Optional, Dict, Any, Union


class PRCClient:
    """
    A client to interact with the Police Roleplay Community (PRC) API.
    """

    BASE_URL = "https://api.policeroleplay.community/v1"

    def __init__(self, server_key: str, global_api_key: Optional[str] = None):
        self.server_key = server_key
        self.global_api_key = global_api_key

    def _build_headers(self) -> Dict[str, str]:
        headers = {
            "Server-Key": self.server_key,
            "Accept": "application/json",
        }
        if self.global_api_key:
            headers["authorization"] = self.global_api_key
        return headers

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            data = response.json()
        except ValueError:
            return {
                "success": False,
                "status_code": response.status_code,
                "error_message": f"Invalid JSON response: {response.text}",
                "data": None,
            }

        if isinstance(data, dict) and data.get("error_code", 0) != 0:
            return {
                "success": False,
                "status_code": response.status_code,
                "error_message": data.get("error", "Unknown error"),
                "error_code": data.get("error_code", 0),
                "data": data,
            }

        return {
            "success": True,
            "status_code": response.status_code,
            "data": data,
        }

    def _request(self, method: str, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._build_headers()

        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=payload)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        except requests.RequestException as e:
            return {
                "success": False,
                "status_code": 0,
                "error_message": str(e),
                "data": None,
            }

        return self._handle_response(response)

    # API Methods
    def get_server_status(self):
        return self._request("GET", "/server")

    def get_players(self):
        return self._request("GET", "/server/players")

    def get_join_logs(self):
        return self._request("GET", "/server/joinlogs")

    def get_kill_logs(self):
        return self._request("GET", "/server/killlogs")

    def get_command_logs(self):
        return self._request("GET", "/server/commandlogs")

    def get_mod_calls(self):
        return self._request("GET", "/server/modcalls")

    def get_queue(self):
        return self._request("GET", "/server/queue")

    def get_bans(self):
        return self._request("GET", "/server/bans")

    def get_vehicles(self):
        return self._request("GET", "/server/vehicles")

    def run_command(self, command: str):
        return self._request("POST", "/server/command", payload={"command": command})
