import user_agents
from datetime import datetime, timezone
from dataclasses import dataclass, field
import uuid


@dataclass
class UserSession:
    ip_address: str
    user_agent_string: str
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: datetime | None = None
    os_platform: str = "Unknown"

    def __post_init__(self):
        """Parse user-agent string to identify OS platform upon creation."""
        self.os_platform = self._parse_os(self.user_agent_string)

    @staticmethod
    def _parse_os(user_agent_str: str) -> str:
        ua = user_agents.parse(user_agent_str)

        if ua.is_android or "Android" in user_agent_str:
            return "android"
        elif ua.is_ios or any(x in user_agent_str for x in ["iPhone", "iPad", "iPod"]):
            return "ios"
        elif "Windows" in ua.os.family or "Windows" in user_agent_str:
            return "windows"
        elif "Linux" in ua.os.family or "Linux" in user_agent_str:
            return "linux"

        return "unknown"

    def end_session(self) -> None:
        """Mark session completion."""
        self.end_time = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """Serialize payload for microservices (JSON-compatible)."""
        duration = None
        if self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()

        return {
            "session_id": self.session_id,
            "ip_address": self.ip_address,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": duration,
            "os_platform": self.os_platform,
        }



# End of file
