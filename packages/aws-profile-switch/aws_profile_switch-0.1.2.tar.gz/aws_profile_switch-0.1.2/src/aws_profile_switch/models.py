"""Data models for AWS Profile Switch."""

from dataclasses import dataclass
from typing import Dict, List, Optional
import json
from pathlib import Path


@dataclass
class SSOProfile:
    """Represents an AWS SSO profile."""
    
    profile_name: str
    sso_account_name: str
    sso_account_id: str
    sso_role_name: str
    sso_start_url: str
    sso_region: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Validate required fields after initialization."""
        if not all([
            self.profile_name,
            self.sso_account_name,
            self.sso_account_id,
            self.sso_role_name,
            self.sso_start_url
        ]):
            raise ValueError("All required SSO fields must be provided")
    
    @property
    def display_name(self) -> str:
        """Get a formatted display name for the profile."""
        return f"{self.sso_account_name} - {self.sso_role_name}"
    
    def to_dict(self) -> Dict[str, str]:
        """Convert the profile to a dictionary."""
        return {
            "profile_name": self.profile_name,
            "sso_account_name": self.sso_account_name,
            "sso_account_id": self.sso_account_id,
            "sso_role_name": self.sso_role_name,
            "sso_start_url": self.sso_start_url,
            "sso_region": self.sso_region or "",
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "SSOProfile":
        """Create an SSOProfile from a dictionary."""
        return cls(
            profile_name=data["profile_name"],
            sso_account_name=data["sso_account_name"],
            sso_account_id=data["sso_account_id"],
            sso_role_name=data["sso_role_name"],
            sso_start_url=data["sso_start_url"],
            sso_region=data.get("sso_region") or None,
        )


class ProfileHistory:
    """Manages the history of recently used profiles."""
    
    def __init__(self, history_file: Optional[Path] = None):
        """Initialize the profile history manager."""
        self.history_file = history_file or Path.home() / ".aws" / "profile_switch_history.json"
        self._history: List[str] = []
        self._load_history()
    
    def _load_history(self) -> None:
        """Load history from the JSON file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self._history = data.get("recent_profiles", [])
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            self._history = []
    
    def _save_history(self) -> None:
        """Save history to the JSON file."""
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump({"recent_profiles": self._history}, f, indent=2)
        except Exception:
            # Silently fail if we can't save history
            pass
    
    def add_profile(self, profile_name: str) -> None:
        """Add a profile to the history."""
        # Remove the profile if it already exists
        if profile_name in self._history:
            self._history.remove(profile_name)
        
        # Add to the beginning of the list
        self._history.insert(0, profile_name)
        
        # Keep only the last 10 profiles
        self._history = self._history[:10]
        
        # Save the updated history
        self._save_history()
    
    def get_recent_profiles(self, limit: int = 5) -> List[str]:
        """Get the most recently used profiles."""
        return self._history[:limit]
    
    def clear(self) -> None:
        """Clear all history."""
        self._history = []
        self._save_history()