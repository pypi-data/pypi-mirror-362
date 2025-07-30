# pyerlc

**pyerlc** is a lightweight Python wrapper for the [Emergency Response: Liberty County (ERLC)](https://policeroleplay.community/) Police Roleplay Community (PRC) API. It allows you to interact programmatically with your PRC server, providing access to live server data and admin controls.

## Features

- ✅ Get server status
- 👥 Fetch player lists and join logs
- 🔫 Retrieve kill and command logs
- 🚓 View active vehicles and bans
- 🛑 See moderation calls and queue status
- 🧠 Run in-game commands remotely

## Installation

```bash
pip install pyerlc
````

> **Requires:** Python 3.12 or higher

## Usage

```python
from pyerlc import PRCClient

client = PRCClient(server_key="your_server_key", global_api_key="your_global_api_key")

# Get server status
status = client.get_server_status()
print(status)

# Run an in-game command
response = client.run_command("announce Hello from pyerlc!")
print(response)
```
> Please only use a 'global_api_key' if you have been provided with one.

## API Methods

| Method                      | Description                           |
| --------------------------- | ------------------------------------- |
| `get_server_status()`       | Returns general info about the server |
| `get_players()`             | Lists all players currently online    |
| `get_join_logs()`           | Returns recent player join logs       |
| `get_kill_logs()`           | Returns recent player kill logs       |
| `get_command_logs()`        | Lists executed commands               |
| `get_mod_calls()`           | Shows active mod calls                |
| `get_queue()`               | Lists users in the server queue       |
| `get_bans()`                | Retrieves the ban list                |
| `get_vehicles()`            | Lists vehicles currently spawned      |
| `run_command(command: str)` | Runs a command on the server          |

## Error Handling

All methods return a dictionary with the following structure:

```python
{
    "success": True or False,
    "status_code": 200,
    "data": {...} or None,
    "error_message": "Optional error message",
    "error_code": 0  # only present if returned by the API
}
```

## Contributing

Contributions are welcome! Submit a PR or open an issue on GitHub.

## Links

* 📦 PyPI: [pyerlc on PyPI](https://pypi.org/project/pyerlc)
* 🏠 Website: [epelldevelopment.xyz](https://epelldevelopment.xyz)
* 📨 Contact: [epell1@epelldevelopment.xyz](mailto:epell1@epelldevelopment.xyz)
* 🔗 GitHub: [github.com/epell-development/erlc\_py](https://github.com/epell-development/erlc_py)

## License

This project is licensed under the [MIT License](LICENSE).

---

> Built and maintained with 💙 by epell Development
> Product of Australia 🇦🇺
