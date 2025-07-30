"""
Data models for the PRC API Wrapper.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Dict, List
from datetime import datetime


class ErrorCode(Enum):
    """Enumeration of PRC API error codes."""
    UNKNOWN = 0
    ROBLOX_COMM_ERROR = 1001
    INTERNAL_ERROR = 1002
    NO_SERVER_KEY = 2000
    INVALID_SERVER_KEY_FORMAT = 2001
    INVALID_SERVER_KEY = 2002
    INVALID_GLOBAL_API_KEY = 2003
    BANNED_SERVER_KEY = 2004
    INVALID_COMMAND = 3001
    SERVER_OFFLINE = 3002
    RATE_LIMITED = 4001
    RESTRICTED_COMMAND = 4002
    PROHIBITED_MESSAGE = 4003
    RESTRICTED_RESOURCE = 9998
    OUTDATED_MODULE = 9999


@dataclass
class PRCResponse:
    """Response object for PRC API calls."""
    success: bool
    status_code: int
    data: Optional[Any] = None
    error_code: Optional[ErrorCode] = None
    error_message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

    def __bool__(self) -> bool:
        return self.success


@dataclass
class Player:
    """Represents a player on the server."""
    player: str
    team: str
    permission: str
    callsign: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        return cls(
            player=data.get("Player", ""),
            team=data.get("Team", ""),
            permission=data.get("Permission", ""),
            callsign=data.get("Callsign", ""),
        )


@dataclass
class ServerStatus:
    """Represents server status information."""
    name: str
    owner_id: int
    co_owner_ids: List[int]
    current_players: int
    max_players: int
    join_key: str
    acc_verified_req: bool
    team_balance: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServerStatus":
        return cls(
            name=data.get("Name", ""),
            owner_id=data.get("OwnerId", 0),
            co_owner_ids=data.get("CoOwnerIds", []),
            current_players=data.get("CurrentPlayers", 0),
            max_players=data.get("MaxPlayers", 0),
            join_key=data.get("JoinKey", ""),
            acc_verified_req=data.get("AccVerifiedReq", False),
            team_balance=data.get("TeamBalance", False),
        )


@dataclass
class JoinLog:
    """Represents a join/leave log entry."""
    join: bool
    timestamp: datetime
    player: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JoinLog":
        ts = data.get("Timestamp", 0)
        return cls(
            join=data.get("Join", False),
            timestamp=datetime.fromtimestamp(ts),
            player=data.get("Player", ""),
        )


@dataclass
class KillLog:
    """Represents a kill log entry."""
    timestamp: datetime
    killer: str
    killed: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KillLog":
        ts = data.get("Timestamp", 0)
        return cls(
            timestamp=datetime.fromtimestamp(ts),
            killer=data.get("Killer", ""),
            killed=data.get("Killed", ""),
        )


@dataclass
class CommandLog:
    """Represents a command log entry."""
    timestamp: datetime
    player: str
    command: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CommandLog":
        ts = data.get("Timestamp", 0)
        return cls(
            timestamp=datetime.fromtimestamp(ts),
            player=data.get("Player", ""),
            command=data.get("Command", ""),
        )


@dataclass
class ModCall:
    """Represents a moderator call."""
    timestamp: datetime
    caller: str
    moderator: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModCall":
        ts = data.get("Timestamp", 0)
        return cls(
            timestamp=datetime.fromtimestamp(ts),
            caller=data.get("Caller", ""),
            moderator=data.get("Moderator"),
        )


@dataclass
class Vehicle:
    """Represents a spawned vehicle."""
    name: str
    owner: str
    texture: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vehicle":
        return cls(
            name=data.get("Name", ""),
            owner=data.get("Owner", ""),
            texture=data.get("Texture", ""),
        )
