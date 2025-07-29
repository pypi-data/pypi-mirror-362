"""Tests for core functionality."""

import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from aws_profile_switch.core import AWSProfileSwitcher
from aws_profile_switch.exceptions import NoSSOProfilesFoundError
from aws_profile_switch.models import SSOProfile


class TestAWSProfileSwitcher:
    """Tests for AWSProfileSwitcher class."""
    
    def create_test_config(self, content: str) -> Path:
        """Create a temporary config file with the given content."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.config')
        temp_file.write(content)
        temp_file.flush()
        return Path(temp_file.name)
    
    def test_init(self):
        """Test initializing AWSProfileSwitcher."""
        config_file = Path("/test/config")
        switcher = AWSProfileSwitcher(config_file)
        
        assert switcher.config_parser.config_file == config_file
        assert switcher.history is not None
        assert switcher.shell_detector is not None
        assert switcher.profiles == []
        assert switcher.selector is None
    
    def test_init_default_config(self):
        """Test initializing with default config file."""
        switcher = AWSProfileSwitcher()
        
        expected_config = Path.home() / ".aws" / "config"
        assert switcher.config_parser.config_file == expected_config
    
    def test_load_profiles_success(self):
        """Test successfully loading profiles."""
        config_content = """
[profile test-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Test Account
"""
        
        config_file = self.create_test_config(config_content)
        switcher = AWSProfileSwitcher(config_file)
        
        try:
            switcher._load_profiles()
            
            assert len(switcher.profiles) == 1
            assert switcher.profiles[0].profile_name == "test-profile"
            assert switcher.selector is not None
            
        finally:
            config_file.unlink()
    
    def test_load_profiles_no_sso_profiles(self):
        """Test loading config with no SSO profiles."""
        config_content = """
[profile regular-profile]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
region = us-east-1
"""
        
        config_file = self.create_test_config(config_content)
        switcher = AWSProfileSwitcher(config_file)
        
        try:
            with pytest.raises(NoSSOProfilesFoundError):
                switcher._load_profiles()
                
        finally:
            config_file.unlink()
    
    def test_run_with_recent_profile_selection(self):
        """Test running with recent profile selection."""
        config_content = """
[profile test-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Test Account
"""
        
        config_file = self.create_test_config(config_content)
        switcher = AWSProfileSwitcher(config_file)
        
        try:
            with patch.object(switcher.history, 'get_recent_profiles', return_value=["test-profile"]):
                with patch.object(switcher, '_load_profiles'):
                    switcher.profiles = [SSOProfile(
                        profile_name="test-profile",
                        sso_account_name="Test Account",
                        sso_account_id="123456789012",
                        sso_role_name="AdministratorAccess",
                        sso_start_url="https://example.awsapps.com/start"
                    )]
                    
                    mock_selector = MagicMock()
                    mock_selector.show_recent_profiles.return_value = "test-profile"
                    switcher.selector = mock_selector
                    
                    with patch.object(switcher.history, 'add_profile') as mock_add_profile:
                        result = switcher.run()
                        
                        assert result == "test-profile"
                        mock_add_profile.assert_called_once_with("test-profile")
                        
        finally:
            config_file.unlink()
    
    def test_run_full_workflow(self):
        """Test running the full workflow."""
        config_content = """
[profile test-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Test Account
"""
        
        config_file = self.create_test_config(config_content)
        switcher = AWSProfileSwitcher(config_file)
        
        try:
            with patch.object(switcher.history, 'get_recent_profiles', return_value=[]):
                with patch.object(switcher, '_load_profiles'):
                    switcher.profiles = [SSOProfile(
                        profile_name="test-profile",
                        sso_account_name="Test Account",
                        sso_account_id="123456789012",
                        sso_role_name="AdministratorAccess",
                        sso_start_url="https://example.awsapps.com/start"
                    )]
                    
                    mock_selector = MagicMock()
                    mock_selector.show_recent_profiles.return_value = None
                    mock_selector.search_accounts.return_value = "Test Account"
                    mock_selector.search_roles.return_value = "AdministratorAccess"
                    mock_selector.select_profile.return_value = "test-profile"
                    switcher.selector = mock_selector
                    
                    with patch.object(switcher.history, 'add_profile') as mock_add_profile:
                        result = switcher.run()
                        
                        assert result == "test-profile"
                        mock_add_profile.assert_called_once_with("test-profile")
                        mock_selector.search_accounts.assert_called_once()
                        mock_selector.search_roles.assert_called_once_with("Test Account")
                        mock_selector.select_profile.assert_called_once_with("Test Account", "AdministratorAccess")
                        
        finally:
            config_file.unlink()
    
    def test_run_user_cancellation_at_account_search(self):
        """Test user cancelling at account search."""
        config_content = """
[profile test-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Test Account
"""
        
        config_file = self.create_test_config(config_content)
        switcher = AWSProfileSwitcher(config_file)
        
        try:
            with patch.object(switcher.history, 'get_recent_profiles', return_value=[]):
                with patch.object(switcher, '_load_profiles'):
                    switcher.profiles = [SSOProfile(
                        profile_name="test-profile",
                        sso_account_name="Test Account",
                        sso_account_id="123456789012",
                        sso_role_name="AdministratorAccess",
                        sso_start_url="https://example.awsapps.com/start"
                    )]
                    
                    mock_selector = MagicMock()
                    mock_selector.show_recent_profiles.return_value = None
                    mock_selector.search_accounts.return_value = None  # User cancelled
                    switcher.selector = mock_selector
                    
                    result = switcher.run()
                    
                    assert result is None
                    mock_selector.search_accounts.assert_called_once()
                    mock_selector.search_roles.assert_not_called()
                    
        finally:
            config_file.unlink()
    
    def test_run_user_cancellation_at_role_search(self):
        """Test user cancelling at role search."""
        config_content = """
[profile test-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Test Account
"""
        
        config_file = self.create_test_config(config_content)
        switcher = AWSProfileSwitcher(config_file)
        
        try:
            with patch.object(switcher.history, 'get_recent_profiles', return_value=[]):
                with patch.object(switcher, '_load_profiles'):
                    switcher.profiles = [SSOProfile(
                        profile_name="test-profile",
                        sso_account_name="Test Account",
                        sso_account_id="123456789012",
                        sso_role_name="AdministratorAccess",
                        sso_start_url="https://example.awsapps.com/start"
                    )]
                    
                    mock_selector = MagicMock()
                    mock_selector.show_recent_profiles.return_value = None
                    mock_selector.search_accounts.return_value = "Test Account"
                    mock_selector.search_roles.return_value = None  # User cancelled
                    switcher.selector = mock_selector
                    
                    result = switcher.run()
                    
                    assert result is None
                    mock_selector.search_accounts.assert_called_once()
                    mock_selector.search_roles.assert_called_once_with("Test Account")
                    mock_selector.select_profile.assert_not_called()
                    
        finally:
            config_file.unlink()
    
    def test_get_shell_command(self):
        """Test getting shell command."""
        switcher = AWSProfileSwitcher()
        
        with patch.object(switcher.shell_detector, 'generate_export_command', return_value='export AWS_PROFILE="test-profile"'):
            command = switcher.get_shell_command("test-profile")
            
            assert command == 'export AWS_PROFILE="test-profile"'
            switcher.shell_detector.generate_export_command.assert_called_once_with("test-profile")
    
    def test_get_profile_info_existing(self):
        """Test getting profile info for existing profile."""
        config_content = """
[profile test-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Test Account
"""
        
        config_file = self.create_test_config(config_content)
        switcher = AWSProfileSwitcher(config_file)
        
        try:
            switcher._load_profiles()
            
            profile_info = switcher.get_profile_info("test-profile")
            
            assert profile_info is not None
            assert profile_info["profile_name"] == "test-profile"
            assert profile_info["sso_account_name"] == "Test Account"
            assert profile_info["sso_account_id"] == "123456789012"
            assert profile_info["sso_role_name"] == "AdministratorAccess"
            
        finally:
            config_file.unlink()
    
    def test_get_profile_info_nonexistent(self):
        """Test getting profile info for non-existent profile."""
        config_content = """
[profile test-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Test Account
"""
        
        config_file = self.create_test_config(config_content)
        switcher = AWSProfileSwitcher(config_file)
        
        try:
            switcher._load_profiles()
            
            profile_info = switcher.get_profile_info("nonexistent-profile")
            
            assert profile_info is None
            
        finally:
            config_file.unlink()
    
    def test_list_profiles(self):
        """Test listing all profiles."""
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
sso_account_id = 123456789013
sso_role_name = ReadOnlyAccess
sso_account_name = Account 2
"""
        
        config_file = self.create_test_config(config_content)
        switcher = AWSProfileSwitcher(config_file)
        
        try:
            profiles = switcher.list_profiles()
            
            assert len(profiles) == 2
            
            profile_names = [p["profile_name"] for p in profiles]
            assert "profile1" in profile_names
            assert "profile2" in profile_names
            
            # Check the structure of the returned data
            for profile in profiles:
                assert "profile_name" in profile
                assert "account_name" in profile
                assert "account_id" in profile
                assert "role_name" in profile
                assert "display_name" in profile
                
        finally:
            config_file.unlink()
    
    def test_list_profiles_empty(self):
        """Test listing profiles when none exist."""
        config_content = """
[profile regular-profile]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
region = us-east-1
"""
        
        config_file = self.create_test_config(config_content)
        switcher = AWSProfileSwitcher(config_file)
        
        try:
            with pytest.raises(NoSSOProfilesFoundError):
                switcher.list_profiles()
                
        finally:
            config_file.unlink()