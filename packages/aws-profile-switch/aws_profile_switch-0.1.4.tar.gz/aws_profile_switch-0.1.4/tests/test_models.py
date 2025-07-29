"""Tests for AWS Profile Switch models."""

import json
import tempfile
from pathlib import Path
import pytest

from aws_profile_switch.models import SSOProfile, ProfileHistory


class TestSSOProfile:
    """Tests for SSOProfile model."""
    
    def test_sso_profile_creation(self):
        """Test creating a valid SSO profile."""
        profile = SSOProfile(
            profile_name="test-profile",
            sso_account_name="Test Account",
            sso_account_id="123456789012",
            sso_role_name="AdministratorAccess",
            sso_start_url="https://example.awsapps.com/start"
        )
        
        assert profile.profile_name == "test-profile"
        assert profile.sso_account_name == "Test Account"
        assert profile.sso_account_id == "123456789012"
        assert profile.sso_role_name == "AdministratorAccess"
        assert profile.sso_start_url == "https://example.awsapps.com/start"
        assert profile.sso_region is None
    
    def test_sso_profile_with_region(self):
        """Test creating an SSO profile with region."""
        profile = SSOProfile(
            profile_name="test-profile",
            sso_account_name="Test Account",
            sso_account_id="123456789012",
            sso_role_name="AdministratorAccess",
            sso_start_url="https://example.awsapps.com/start",
            sso_region="us-west-2"
        )
        
        assert profile.sso_region == "us-west-2"
    
    def test_sso_profile_invalid_missing_fields(self):
        """Test that creating a profile with missing required fields raises ValueError."""
        with pytest.raises(ValueError, match="All required SSO fields must be provided"):
            SSOProfile(
                profile_name="",
                sso_account_name="Test Account",
                sso_account_id="123456789012",
                sso_role_name="AdministratorAccess",
                sso_start_url="https://example.awsapps.com/start"
            )
    
    def test_display_name(self):
        """Test the display name property."""
        profile = SSOProfile(
            profile_name="test-profile",
            sso_account_name="Test Account",
            sso_account_id="123456789012",
            sso_role_name="AdministratorAccess",
            sso_start_url="https://example.awsapps.com/start"
        )
        
        assert profile.display_name == "Test Account - AdministratorAccess"
    
    def test_to_dict(self):
        """Test converting profile to dictionary."""
        profile = SSOProfile(
            profile_name="test-profile",
            sso_account_name="Test Account",
            sso_account_id="123456789012",
            sso_role_name="AdministratorAccess",
            sso_start_url="https://example.awsapps.com/start",
            sso_region="us-west-2"
        )
        
        expected = {
            "profile_name": "test-profile",
            "sso_account_name": "Test Account",
            "sso_account_id": "123456789012",
            "sso_role_name": "AdministratorAccess",
            "sso_start_url": "https://example.awsapps.com/start",
            "sso_region": "us-west-2",
        }
        
        assert profile.to_dict() == expected
    
    def test_from_dict(self):
        """Test creating profile from dictionary."""
        data = {
            "profile_name": "test-profile",
            "sso_account_name": "Test Account",
            "sso_account_id": "123456789012",
            "sso_role_name": "AdministratorAccess",
            "sso_start_url": "https://example.awsapps.com/start",
            "sso_region": "us-west-2",
        }
        
        profile = SSOProfile.from_dict(data)
        
        assert profile.profile_name == "test-profile"
        assert profile.sso_account_name == "Test Account"
        assert profile.sso_account_id == "123456789012"
        assert profile.sso_role_name == "AdministratorAccess"
        assert profile.sso_start_url == "https://example.awsapps.com/start"
        assert profile.sso_region == "us-west-2"


class TestProfileHistory:
    """Tests for ProfileHistory class."""
    
    def test_profile_history_init(self):
        """Test initializing profile history."""
        with tempfile.TemporaryDirectory() as temp_dir:
            history_file = Path(temp_dir) / "history.json"
            history = ProfileHistory(history_file)
            
            assert history.history_file == history_file
            assert history.get_recent_profiles() == []
    
    def test_add_profile(self):
        """Test adding a profile to history."""
        with tempfile.TemporaryDirectory() as temp_dir:
            history_file = Path(temp_dir) / "history.json"
            history = ProfileHistory(history_file)
            
            history.add_profile("profile1")
            history.add_profile("profile2")
            
            recent = history.get_recent_profiles()
            assert recent == ["profile2", "profile1"]
    
    def test_add_duplicate_profile(self):
        """Test adding a duplicate profile moves it to front."""
        with tempfile.TemporaryDirectory() as temp_dir:
            history_file = Path(temp_dir) / "history.json"
            history = ProfileHistory(history_file)
            
            history.add_profile("profile1")
            history.add_profile("profile2")
            history.add_profile("profile1")  # Duplicate
            
            recent = history.get_recent_profiles()
            assert recent == ["profile1", "profile2"]
    
    def test_history_limit(self):
        """Test that history is limited to 10 profiles."""
        with tempfile.TemporaryDirectory() as temp_dir:
            history_file = Path(temp_dir) / "history.json"
            history = ProfileHistory(history_file)
            
            # Add 15 profiles
            for i in range(15):
                history.add_profile(f"profile{i}")
            
            recent = history.get_recent_profiles(limit=20)
            assert len(recent) == 10
            assert recent[0] == "profile14"  # Most recent
            assert recent[-1] == "profile5"  # Oldest kept
    
    def test_get_recent_profiles_limit(self):
        """Test limiting the number of recent profiles returned."""
        with tempfile.TemporaryDirectory() as temp_dir:
            history_file = Path(temp_dir) / "history.json"
            history = ProfileHistory(history_file)
            
            for i in range(10):
                history.add_profile(f"profile{i}")
            
            recent = history.get_recent_profiles(limit=3)
            assert len(recent) == 3
            assert recent == ["profile9", "profile8", "profile7"]
    
    def test_clear_history(self):
        """Test clearing all history."""
        with tempfile.TemporaryDirectory() as temp_dir:
            history_file = Path(temp_dir) / "history.json"
            history = ProfileHistory(history_file)
            
            history.add_profile("profile1")
            history.add_profile("profile2")
            
            assert len(history.get_recent_profiles()) == 2
            
            history.clear()
            assert history.get_recent_profiles() == []
    
    def test_persistence(self):
        """Test that history is persisted to disk."""
        with tempfile.TemporaryDirectory() as temp_dir:
            history_file = Path(temp_dir) / "history.json"
            
            # Create history and add profiles
            history1 = ProfileHistory(history_file)
            history1.add_profile("profile1")
            history1.add_profile("profile2")
            
            # Create new history instance and verify profiles are loaded
            history2 = ProfileHistory(history_file)
            recent = history2.get_recent_profiles()
            assert recent == ["profile2", "profile1"]
    
    def test_load_corrupted_history(self):
        """Test loading corrupted history file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            history_file = Path(temp_dir) / "history.json"
            
            # Create corrupted JSON file
            with open(history_file, 'w') as f:
                f.write("invalid json")
            
            # Should handle corrupted file gracefully
            history = ProfileHistory(history_file)
            assert history.get_recent_profiles() == []
    
    def test_load_missing_history(self):
        """Test loading from non-existent history file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            history_file = Path(temp_dir) / "nonexistent.json"
            history = ProfileHistory(history_file)
            
            assert history.get_recent_profiles() == []