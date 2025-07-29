"""Tests for AWS config parser."""

import tempfile
from pathlib import Path
import pytest

from aws_profile_switch.config_parser import AWSConfigParser
from aws_profile_switch.exceptions import ConfigFileNotFoundError, ConfigParseError, InvalidProfileError


class TestAWSConfigParser:
    """Tests for AWSConfigParser class."""
    
    def create_test_config(self, content: str) -> Path:
        """Create a temporary config file with the given content."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.config')
        temp_file.write(content)
        temp_file.flush()
        return Path(temp_file.name)
    
    def test_parse_valid_sso_profile(self):
        """Test parsing a valid SSO profile."""
        config_content = """
[profile test-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Test Account
region = us-east-1
output = json
"""
        
        config_file = self.create_test_config(config_content)
        parser = AWSConfigParser(config_file)
        
        try:
            profiles = parser.parse_config()
            
            assert len(profiles) == 1
            profile = profiles[0]
            
            assert profile.profile_name == "test-profile"
            assert profile.sso_account_name == "Test Account"
            assert profile.sso_account_id == "123456789012"
            assert profile.sso_role_name == "AdministratorAccess"
            assert profile.sso_start_url == "https://example.awsapps.com/start"
            assert profile.sso_region == "us-east-1"
            
        finally:
            config_file.unlink()
    
    def test_parse_sso_auto_populated_profile(self):
        """Test parsing a profile with sso_auto_populated flag."""
        config_content = """
[profile auto-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = ReadOnlyAccess
sso_auto_populated = true
region = us-east-1
output = json
"""
        
        config_file = self.create_test_config(config_content)
        parser = AWSConfigParser(config_file)
        
        try:
            profiles = parser.parse_config()
            
            assert len(profiles) == 1
            profile = profiles[0]
            
            assert profile.profile_name == "auto-profile"
            assert profile.sso_role_name == "ReadOnlyAccess"
            
        finally:
            config_file.unlink()
    
    def test_parse_profile_without_account_name(self):
        """Test parsing a profile without explicit account name."""
        config_content = """
[profile no-account-name]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
region = us-east-1
output = json
"""
        
        config_file = self.create_test_config(config_content)
        parser = AWSConfigParser(config_file)
        
        try:
            profiles = parser.parse_config()
            
            assert len(profiles) == 1
            profile = profiles[0]
            
            assert profile.profile_name == "no-account-name"
            assert profile.sso_account_name == "Account-123456789012"  # Generated name
            
        finally:
            config_file.unlink()
    
    def test_parse_multiple_profiles(self):
        """Test parsing multiple SSO profiles."""
        config_content = """
[profile profile1]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Account 1
region = us-east-1

[profile profile2]
sso_start_url = https://example.awsapps.com/start
sso_region = us-west-2
sso_account_id = 123456789013
sso_role_name = ReadOnlyAccess
sso_account_name = Account 2
region = us-west-2

[profile non-sso-profile]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
region = us-east-1
"""
        
        config_file = self.create_test_config(config_content)
        parser = AWSConfigParser(config_file)
        
        try:
            profiles = parser.parse_config()
            
            assert len(profiles) == 2  # Only SSO profiles
            
            profile_names = [p.profile_name for p in profiles]
            assert "profile1" in profile_names
            assert "profile2" in profile_names
            assert "non-sso-profile" not in profile_names
            
        finally:
            config_file.unlink()
    
    def test_parse_invalid_profile_missing_fields(self):
        """Test parsing a profile with missing required SSO fields."""
        config_content = """
[profile incomplete-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
# Missing sso_account_id and sso_role_name
region = us-east-1
"""
        
        config_file = self.create_test_config(config_content)
        parser = AWSConfigParser(config_file)
        
        try:
            profiles = parser.parse_config()
            
            # Should skip invalid profiles
            assert len(profiles) == 0
            
        finally:
            config_file.unlink()
    
    def test_parse_nonexistent_file(self):
        """Test parsing a non-existent config file."""
        parser = AWSConfigParser(Path("/nonexistent/config"))
        
        with pytest.raises(ConfigFileNotFoundError):
            parser.parse_config()
    
    def test_parse_invalid_config_format(self):
        """Test parsing a config file with invalid format."""
        config_content = """
This is not a valid config file format
[profile incomplete
missing closing bracket
"""
        
        config_file = self.create_test_config(config_content)
        parser = AWSConfigParser(config_file)
        
        try:
            with pytest.raises(ConfigParseError):
                parser.parse_config()
                
        finally:
            config_file.unlink()
    
    def test_get_profile_by_name(self):
        """Test getting a profile by name."""
        config_content = """
[profile test-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Test Account
"""
        
        config_file = self.create_test_config(config_content)
        parser = AWSConfigParser(config_file)
        
        try:
            parser.parse_config()
            
            profile = parser.get_profile_by_name("test-profile")
            assert profile is not None
            assert profile.profile_name == "test-profile"
            
            profile = parser.get_profile_by_name("nonexistent")
            assert profile is None
            
        finally:
            config_file.unlink()
    
    def test_get_accounts(self):
        """Test getting unique account names."""
        config_content = """
[profile profile1]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Account 1

[profile profile2]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = ReadOnlyAccess
sso_account_name = Account 1

[profile profile3]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789013
sso_role_name = AdministratorAccess
sso_account_name = Account 2
"""
        
        config_file = self.create_test_config(config_content)
        parser = AWSConfigParser(config_file)
        
        try:
            parser.parse_config()
            
            accounts = parser.get_accounts()
            assert len(accounts) == 2
            assert "Account 1" in accounts
            assert "Account 2" in accounts
            
        finally:
            config_file.unlink()
    
    def test_get_roles_for_account(self):
        """Test getting roles for a specific account."""
        config_content = """
[profile profile1]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Account 1

[profile profile2]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = ReadOnlyAccess
sso_account_name = Account 1

[profile profile3]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789013
sso_role_name = AdministratorAccess
sso_account_name = Account 2
"""
        
        config_file = self.create_test_config(config_content)
        parser = AWSConfigParser(config_file)
        
        try:
            parser.parse_config()
            
            roles = parser.get_roles_for_account("Account 1")
            assert len(roles) == 2
            assert "AdministratorAccess" in roles
            assert "ReadOnlyAccess" in roles
            
            roles = parser.get_roles_for_account("Account 2")
            assert len(roles) == 1
            assert "AdministratorAccess" in roles
            
            roles = parser.get_roles_for_account("Nonexistent Account")
            assert len(roles) == 0
            
        finally:
            config_file.unlink()
    
    def test_get_profiles_for_account_and_role(self):
        """Test getting profiles for a specific account and role."""
        config_content = """
[profile profile1]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Account 1

[profile profile2]
sso_start_url = https://example.awsapps.com/start
sso_region = us-west-2
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Account 1

[profile profile3]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789013
sso_role_name = AdministratorAccess
sso_account_name = Account 2
"""
        
        config_file = self.create_test_config(config_content)
        parser = AWSConfigParser(config_file)
        
        try:
            parser.parse_config()
            
            profiles = parser.get_profiles_for_account_and_role("Account 1", "AdministratorAccess")
            assert len(profiles) == 2
            
            profile_names = [p.profile_name for p in profiles]
            assert "profile1" in profile_names
            assert "profile2" in profile_names
            
            profiles = parser.get_profiles_for_account_and_role("Account 2", "AdministratorAccess")
            assert len(profiles) == 1
            assert profiles[0].profile_name == "profile3"
            
        finally:
            config_file.unlink()