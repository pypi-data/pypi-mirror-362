"""AWS configuration file parser."""

import configparser
import os
from pathlib import Path
from typing import Dict, List, Optional

from .exceptions import ConfigFileNotFoundError, ConfigParseError, InvalidProfileError
from .models import SSOProfile


class AWSConfigParser:
    """Parser for AWS configuration files."""
    
    def __init__(self, config_file: Optional[Path] = None):
        """Initialize the AWS config parser."""
        self.config_file = config_file or Path.home() / ".aws" / "config"
        self.profiles: List[SSOProfile] = []
    
    def _is_sso_profile(self, section: configparser.SectionProxy) -> bool:
        """Check if a configuration section represents an SSO profile."""
        # Check for explicit SSO auto-populated flag
        if section.get("sso_auto_populated", "").lower() == "true":
            return True
        
        # Check for presence of required SSO fields
        sso_fields = [
            "sso_start_url",
            "sso_account_id",
            "sso_role_name"
        ]
        
        return all(field in section for field in sso_fields)
    
    def _extract_sso_profile(self, profile_name: str, section: configparser.SectionProxy) -> SSOProfile:
        """Extract SSO profile information from a configuration section."""
        try:
            # Extract required fields
            sso_start_url = section.get("sso_start_url")
            sso_account_id = section.get("sso_account_id")
            sso_role_name = section.get("sso_role_name")
            
            # Extract optional fields
            sso_region = section.get("sso_region")
            
            # For account name, try multiple sources
            sso_account_name = (
                section.get("sso_account_name") or
                section.get("account_name") or
                f"Account-{sso_account_id}"
            )
            
            # Validate required fields
            if not all([sso_start_url, sso_account_id, sso_role_name]):
                raise InvalidProfileError(f"Profile '{profile_name}' missing required SSO fields")
            
            return SSOProfile(
                profile_name=profile_name,
                sso_account_name=sso_account_name,
                sso_account_id=sso_account_id,
                sso_role_name=sso_role_name,
                sso_start_url=sso_start_url,
                sso_region=sso_region
            )
            
        except (ValueError, InvalidProfileError) as e:
            raise InvalidProfileError(f"Invalid SSO profile '{profile_name}': {e}")
    
    def parse_config(self) -> List[SSOProfile]:
        """Parse the AWS config file and extract SSO profiles."""
        if not self.config_file.exists():
            raise ConfigFileNotFoundError(f"AWS config file not found: {self.config_file}")
        
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file)
            
            profiles = []
            
            for section_name in config.sections():
                # Skip non-profile sections
                if not section_name.startswith("profile "):
                    continue
                
                # Extract profile name (remove "profile " prefix)
                profile_name = section_name[8:]  # len("profile ") = 8
                section = config[section_name]
                
                # Check if this is an SSO profile
                if self._is_sso_profile(section):
                    try:
                        profile = self._extract_sso_profile(profile_name, section)
                        profiles.append(profile)
                    except InvalidProfileError:
                        # Skip invalid profiles but continue processing
                        continue
            
            self.profiles = profiles
            return profiles
            
        except configparser.Error as e:
            raise ConfigParseError(f"Failed to parse AWS config file: {e}")
        except Exception as e:
            raise ConfigParseError(f"Unexpected error parsing config file: {e}")
    
    def get_profiles(self) -> List[SSOProfile]:
        """Get the list of parsed SSO profiles."""
        return self.profiles
    
    def get_profile_by_name(self, profile_name: str) -> Optional[SSOProfile]:
        """Get a specific profile by name."""
        for profile in self.profiles:
            if profile.profile_name == profile_name:
                return profile
        return None
    
    def get_accounts(self) -> List[str]:
        """Get a list of unique account names."""
        return sorted(list(set(profile.sso_account_name for profile in self.profiles)))
    
    def get_roles_for_account(self, account_name: str) -> List[str]:
        """Get a list of roles for a specific account."""
        roles = [
            profile.sso_role_name
            for profile in self.profiles
            if profile.sso_account_name == account_name
        ]
        return sorted(list(set(roles)))
    
    def get_profiles_for_account_and_role(self, account_name: str, role_name: str) -> List[SSOProfile]:
        """Get profiles matching a specific account and role."""
        return [
            profile for profile in self.profiles
            if profile.sso_account_name == account_name and profile.sso_role_name == role_name
        ]