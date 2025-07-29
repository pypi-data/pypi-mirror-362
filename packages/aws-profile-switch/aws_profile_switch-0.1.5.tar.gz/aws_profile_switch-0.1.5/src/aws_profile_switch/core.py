"""Core functionality for AWS Profile Switch."""

from typing import Optional
from pathlib import Path

from .config_parser import AWSConfigParser
from .exceptions import AWSProfileSwitchError, NoSSOProfilesFoundError
from .models import ProfileHistory
from .ui import ProfileSelector
from .shell import ShellDetector


class AWSProfileSwitcher:
    """Main class that orchestrates the profile switching workflow."""
    
    def __init__(self, config_file: Optional[Path] = None):
        """Initialize the AWS Profile Switcher."""
        self.config_parser = AWSConfigParser(config_file)
        self.history = ProfileHistory()
        self.shell_detector = ShellDetector()
        self.profiles = []
        self.selector = None
    
    def _load_profiles(self) -> None:
        """Load and parse AWS profiles from the config file."""
        self.profiles = self.config_parser.parse_config()
        
        if not self.profiles:
            raise NoSSOProfilesFoundError(
                "No SSO profiles found in AWS config file. "
                "Please ensure you have SSO profiles configured."
            )
        
        self.selector = ProfileSelector(self.profiles)
    
    def run(self) -> Optional[str]:
        """Run the interactive profile selection workflow."""
        try:
            # Load profiles
            self._load_profiles()
            
            # Get recent profiles for potential use with arrow keys
            recent_profiles = self.history.get_recent_profiles()
            
            # Step 1: Search for account (with recent profiles available via arrow keys)
            account_name = self.selector.search_accounts_with_history(recent_profiles)
            if not account_name:
                return None  # User cancelled
            
            # Step 2: Search for role within the selected account
            role_name = self.selector.search_roles(account_name)
            if not role_name:
                return None  # User cancelled
            
            # Step 3: Select profile if multiple matches
            profile_name = self.selector.select_profile(account_name, role_name)
            if not profile_name:
                return None  # User cancelled
            
            # Add to history
            self.history.add_profile(profile_name)
            
            return profile_name
            
        except AWSProfileSwitchError:
            # Re-raise application-specific errors
            raise
        except Exception as e:
            # Wrap unexpected errors
            raise AWSProfileSwitchError(f"Unexpected error during profile selection: {e}")
    
    def get_shell_command(self, profile_name: str) -> str:
        """Get the appropriate shell command to set the AWS_PROFILE environment variable."""
        return self.shell_detector.generate_export_command(profile_name)
    
    def get_profile_info(self, profile_name: str) -> Optional[dict]:
        """Get detailed information about a specific profile."""
        profile = self.config_parser.get_profile_by_name(profile_name)
        if profile:
            return profile.to_dict()
        return None
    
    def list_profiles(self) -> list:
        """List all available SSO profiles."""
        if not self.profiles:
            self._load_profiles()
        
        return [
            {
                "profile_name": profile.profile_name,
                "account_name": profile.sso_account_name,
                "account_id": profile.sso_account_id,
                "role_name": profile.sso_role_name,
                "display_name": profile.display_name,
            }
            for profile in self.profiles
        ]