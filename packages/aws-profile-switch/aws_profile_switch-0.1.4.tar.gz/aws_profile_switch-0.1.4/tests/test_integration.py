"""Integration tests for AWS Profile Switch."""

import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from aws_profile_switch.core import AWSProfileSwitcher
from aws_profile_switch.exceptions import ConfigFileNotFoundError, NoSSOProfilesFoundError


class TestIntegration:
    """Integration tests for the complete workflow."""
    
    def create_test_config(self, content: str) -> Path:
        """Create a temporary config file with the given content."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.config')
        temp_file.write(content)
        temp_file.flush()
        return Path(temp_file.name)
    
    def test_full_workflow_with_recent_profiles(self):
        """Test the complete workflow with recent profiles available."""
        config_content = """
[profile dev-admin]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Development Account

[profile prod-readonly]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789013
sso_role_name = ReadOnlyAccess
sso_account_name = Production Account
"""
        
        config_file = self.create_test_config(config_content)
        
        try:
            # Create switcher with temp config and history
            with tempfile.TemporaryDirectory() as temp_dir:
                history_file = Path(temp_dir) / "history.json"
                switcher = AWSProfileSwitcher(config_file)
                switcher.history.history_file = history_file
                
                # Pre-populate history
                switcher.history.add_profile("dev-admin")
                switcher.history.add_profile("prod-readonly")
                
                # Mock UI interactions - user selects recent profile
                with patch.object(switcher, '_load_profiles', wraps=switcher._load_profiles):
                    with patch('aws_profile_switch.ui.ProfileSelector') as mock_selector_class:
                        mock_selector = MagicMock()
                        mock_selector_class.return_value = mock_selector
                        mock_selector.show_recent_profiles.return_value = "prod-readonly"
                        
                        # Run the workflow
                        result = switcher.run()
                        
                        # Verify the result
                        assert result == "prod-readonly"
                        
                        # Verify history was updated
                        recent = switcher.history.get_recent_profiles()
                        assert recent[0] == "prod-readonly"  # Most recent
                        
                        # Verify UI was called correctly
                        mock_selector.show_recent_profiles.assert_called_once()
                        
        finally:
            config_file.unlink()
    
    def test_full_workflow_without_recent_profiles(self):
        """Test the complete workflow without recent profiles."""
        config_content = """
[profile dev-admin]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Development Account

[profile dev-readonly]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = ReadOnlyAccess
sso_account_name = Development Account

[profile prod-admin]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789013
sso_role_name = AdministratorAccess
sso_account_name = Production Account
"""
        
        config_file = self.create_test_config(config_content)
        
        try:
            # Create switcher with temp config and history
            with tempfile.TemporaryDirectory() as temp_dir:
                history_file = Path(temp_dir) / "history.json"
                switcher = AWSProfileSwitcher(config_file)
                switcher.history.history_file = history_file
                
                # Mock UI interactions - no recent profiles, user searches
                with patch.object(switcher, '_load_profiles', wraps=switcher._load_profiles):
                    with patch('aws_profile_switch.ui.ProfileSelector') as mock_selector_class:
                        mock_selector = MagicMock()
                        mock_selector_class.return_value = mock_selector
                        mock_selector.show_recent_profiles.return_value = None  # No recent profiles
                        mock_selector.search_accounts.return_value = "Development Account"
                        mock_selector.search_roles.return_value = "AdministratorAccess"
                        mock_selector.select_profile.return_value = "dev-admin"
                        
                        # Run the workflow
                        result = switcher.run()
                        
                        # Verify the result
                        assert result == "dev-admin"
                        
                        # Verify history was updated
                        recent = switcher.history.get_recent_profiles()
                        assert recent[0] == "dev-admin"
                        
                        # Verify UI flow
                        mock_selector.show_recent_profiles.assert_called_once()
                        mock_selector.search_accounts.assert_called_once()
                        mock_selector.search_roles.assert_called_once_with("Development Account")
                        mock_selector.select_profile.assert_called_once_with("Development Account", "AdministratorAccess")
                        
        finally:
            config_file.unlink()
    
    def test_shell_command_generation_integration(self):
        """Test shell command generation with different environments."""
        config_content = """
[profile test-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Test Account
"""
        
        config_file = self.create_test_config(config_content)
        
        try:
            switcher = AWSProfileSwitcher(config_file)
            
            # Test bash command generation
            with patch('platform.system', return_value='Linux'):
                with patch.dict('os.environ', {'SHELL': '/bin/bash'}):
                    command = switcher.get_shell_command("test-profile")
                    assert command == 'export AWS_PROFILE="test-profile"'
            
            # Test PowerShell command generation
            with patch('platform.system', return_value='Windows'):
                with patch.dict('os.environ', {'PSModulePath': 'C:\\Windows\\PowerShell'}):
                    command = switcher.get_shell_command("test-profile")
                    assert command == '$env:AWS_PROFILE = "test-profile"'
                    
        finally:
            config_file.unlink()
    
    def test_profile_listing_integration(self):
        """Test profile listing functionality."""
        config_content = """
[profile dev-admin]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Development Account

[profile prod-readonly]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789013
sso_role_name = ReadOnlyAccess
sso_account_name = Production Account

[profile regular-profile]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
region = us-east-1
"""
        
        config_file = self.create_test_config(config_content)
        
        try:
            switcher = AWSProfileSwitcher(config_file)
            
            # List profiles
            profiles = switcher.list_profiles()
            
            # Should only include SSO profiles
            assert len(profiles) == 2
            
            profile_names = [p["profile_name"] for p in profiles]
            assert "dev-admin" in profile_names
            assert "prod-readonly" in profile_names
            assert "regular-profile" not in profile_names
            
            # Check profile structure
            for profile in profiles:
                assert "profile_name" in profile
                assert "account_name" in profile
                assert "account_id" in profile
                assert "role_name" in profile
                assert "display_name" in profile
                
        finally:
            config_file.unlink()
    
    def test_error_handling_integration(self):
        """Test error handling in the complete workflow."""
        # Test missing config file
        nonexistent_config = Path("/nonexistent/config")
        switcher = AWSProfileSwitcher(nonexistent_config)
        
        with pytest.raises(ConfigFileNotFoundError):
            switcher.run()
        
        # Test config with no SSO profiles
        config_content = """
[profile regular-profile]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
region = us-east-1
"""
        
        config_file = self.create_test_config(config_content)
        
        try:
            switcher = AWSProfileSwitcher(config_file)
            
            with pytest.raises(NoSSOProfilesFoundError):
                switcher.run()
                
        finally:
            config_file.unlink()
    
    def test_user_cancellation_integration(self):
        """Test user cancellation at various stages."""
        config_content = """
[profile test-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Test Account
"""
        
        config_file = self.create_test_config(config_content)
        
        try:
            switcher = AWSProfileSwitcher(config_file)
            
            # Test cancellation at account search
            with patch.object(switcher, '_load_profiles', wraps=switcher._load_profiles):
                with patch('aws_profile_switch.ui.ProfileSelector') as mock_selector_class:
                    mock_selector = MagicMock()
                    mock_selector_class.return_value = mock_selector
                    mock_selector.show_recent_profiles.return_value = None
                    mock_selector.search_accounts.return_value = None  # User cancelled
                    
                    result = switcher.run()
                    assert result is None
            
            # Test cancellation at role search
            with patch.object(switcher, '_load_profiles', wraps=switcher._load_profiles):
                with patch('aws_profile_switch.ui.ProfileSelector') as mock_selector_class:
                    mock_selector = MagicMock()
                    mock_selector_class.return_value = mock_selector
                    mock_selector.show_recent_profiles.return_value = None
                    mock_selector.search_accounts.return_value = "Test Account"
                    mock_selector.search_roles.return_value = None  # User cancelled
                    
                    result = switcher.run()
                    assert result is None
                    
        finally:
            config_file.unlink()
    
    def test_profile_history_persistence_integration(self):
        """Test that profile history persists across sessions."""
        config_content = """
[profile test-profile]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
sso_account_name = Test Account
"""
        
        config_file = self.create_test_config(config_content)
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                history_file = Path(temp_dir) / "history.json"
                
                # First session - add profile to history
                switcher1 = AWSProfileSwitcher(config_file)
                switcher1.history.history_file = history_file
                switcher1.history.add_profile("test-profile")
                
                # Second session - verify history is loaded
                switcher2 = AWSProfileSwitcher(config_file)
                switcher2.history.history_file = history_file
                
                recent = switcher2.history.get_recent_profiles()
                assert recent == ["test-profile"]
                
        finally:
            config_file.unlink()
    
    @pytest.mark.slow
    def test_large_profile_list_performance(self):
        """Test performance with a large number of profiles."""
        # Generate a large config file
        config_lines = []
        for i in range(100):
            config_lines.extend([
                f"[profile profile-{i:03d}]",
                f"sso_start_url = https://example.awsapps.com/start",
                f"sso_region = us-east-1",
                f"sso_account_id = {123456789000 + i}",
                f"sso_role_name = Role{i % 5}",
                f"sso_account_name = Account {i // 10}",
                "",
            ])
        
        config_content = "\n".join(config_lines)
        config_file = self.create_test_config(config_content)
        
        try:
            switcher = AWSProfileSwitcher(config_file)
            
            # Test that loading profiles doesn't take too long
            import time
            start_time = time.time()
            switcher._load_profiles()
            load_time = time.time() - start_time
            
            assert load_time < 1.0  # Should load within 1 second
            assert len(switcher.profiles) == 100
            
            # Test searching performance
            start_time = time.time()
            accounts = switcher.config_parser.get_accounts()
            search_time = time.time() - start_time
            
            assert search_time < 0.1  # Should search within 100ms
            assert len(accounts) == 10  # 10 unique accounts
            
        finally:
            config_file.unlink()