"""Tests for fuzzy search functionality."""

import pytest

from aws_profile_switch.search import FuzzySearcher
from aws_profile_switch.models import SSOProfile


class TestFuzzySearcher:
    """Tests for FuzzySearcher class."""
    
    def create_test_profiles(self):
        """Create test profiles for search testing."""
        return [
            SSOProfile(
                profile_name="dev-admin",
                sso_account_name="Development Account",
                sso_account_id="123456789012",
                sso_role_name="AdministratorAccess",
                sso_start_url="https://example.awsapps.com/start"
            ),
            SSOProfile(
                profile_name="dev-readonly",
                sso_account_name="Development Account",
                sso_account_id="123456789012",
                sso_role_name="ReadOnlyAccess",
                sso_start_url="https://example.awsapps.com/start"
            ),
            SSOProfile(
                profile_name="prod-admin",
                sso_account_name="Production Account",
                sso_account_id="123456789013",
                sso_role_name="AdministratorAccess",
                sso_start_url="https://example.awsapps.com/start"
            ),
            SSOProfile(
                profile_name="staging-readonly",
                sso_account_name="Staging Environment",
                sso_account_id="123456789014",
                sso_role_name="ReadOnlyAccess",
                sso_start_url="https://example.awsapps.com/start"
            ),
            SSOProfile(
                profile_name="test-developer",
                sso_account_name="Test Account",
                sso_account_id="123456789015",
                sso_role_name="DeveloperAccess",
                sso_start_url="https://example.awsapps.com/start"
            ),
        ]
    
    def test_search_accounts_exact_match(self):
        """Test searching for accounts with exact match."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_accounts("Development Account")
        assert len(results) > 0
        assert "Development Account" in results
    
    def test_search_accounts_partial_match(self):
        """Test searching for accounts with partial match."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_accounts("Dev")
        assert len(results) > 0
        assert "Development Account" in results
    
    def test_search_accounts_fuzzy_match(self):
        """Test searching for accounts with fuzzy match."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_accounts("Developmnt")  # Missing 'e'
        assert len(results) > 0
        assert "Development Account" in results
    
    def test_search_accounts_empty_query(self):
        """Test searching for accounts with empty query."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_accounts("")
        assert len(results) == 0
        
        results = searcher.search_accounts("   ")
        assert len(results) == 0
    
    def test_search_accounts_no_matches(self):
        """Test searching for accounts with no matches."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_accounts("NonexistentAccount")
        assert len(results) == 0
    
    def test_search_accounts_limit(self):
        """Test limiting search results."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_accounts("Account", limit=2)
        assert len(results) <= 2
    
    def test_search_roles_exact_match(self):
        """Test searching for roles with exact match."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_roles("AdministratorAccess", "Development Account")
        assert len(results) > 0
        assert "AdministratorAccess" in results
    
    def test_search_roles_partial_match(self):
        """Test searching for roles with partial match."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_roles("Admin", "Development Account")
        assert len(results) > 0
        assert "AdministratorAccess" in results
    
    def test_search_roles_fuzzy_match(self):
        """Test searching for roles with fuzzy match."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_roles("Readonly", "Development Account")
        assert len(results) > 0
        assert "ReadOnlyAccess" in results
    
    def test_search_roles_account_specific(self):
        """Test that role search is account-specific."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        # Development Account has both Administrator and ReadOnly roles
        results = searcher.search_roles("Access", "Development Account")
        assert len(results) == 2
        assert "AdministratorAccess" in results
        assert "ReadOnlyAccess" in results
        
        # Test Account only has Developer role
        results = searcher.search_roles("Access", "Test Account")
        assert len(results) == 1
        assert "DeveloperAccess" in results
    
    def test_search_roles_empty_query(self):
        """Test searching for roles with empty query."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_roles("", "Development Account")
        assert len(results) == 0
    
    def test_search_roles_nonexistent_account(self):
        """Test searching for roles in a nonexistent account."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_roles("Admin", "Nonexistent Account")
        assert len(results) == 0
    
    def test_search_profiles_exact_match(self):
        """Test searching for profiles with exact match."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_profiles("dev-admin")
        assert len(results) > 0
        assert any(p.profile_name == "dev-admin" for p in results)
    
    def test_search_profiles_account_match(self):
        """Test searching for profiles by account name."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_profiles("Development")
        assert len(results) >= 2  # dev-admin and dev-readonly
        
        profile_names = [p.profile_name for p in results]
        assert "dev-admin" in profile_names
        assert "dev-readonly" in profile_names
    
    def test_search_profiles_role_match(self):
        """Test searching for profiles by role name."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_profiles("Administrator")
        assert len(results) >= 2  # dev-admin and prod-admin
        
        profile_names = [p.profile_name for p in results]
        assert "dev-admin" in profile_names
        assert "prod-admin" in profile_names
    
    def test_search_profiles_empty_query(self):
        """Test searching for profiles with empty query."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_profiles("")
        assert len(results) == 0
    
    def test_search_profiles_limit(self):
        """Test limiting profile search results."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        results = searcher.search_profiles("Account", limit=2)
        assert len(results) <= 2
    
    def test_get_best_match_exact(self):
        """Test getting the best match with exact match."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        candidates = ["Development Account", "Production Account", "Test Account"]
        match, score = searcher.get_best_match("Development Account", candidates)
        
        assert match == "Development Account"
        assert score == 100  # Perfect match
    
    def test_get_best_match_partial(self):
        """Test getting the best match with partial match."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        candidates = ["Development Account", "Production Account", "Test Account"]
        match, score = searcher.get_best_match("Dev", candidates)
        
        assert match == "Development Account"
        assert score > 30  # Should have decent score
    
    def test_get_best_match_empty_query(self):
        """Test getting the best match with empty query."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        candidates = ["Development Account", "Production Account"]
        match, score = searcher.get_best_match("", candidates)
        
        assert match == ""
        assert score == 0
    
    def test_get_best_match_empty_candidates(self):
        """Test getting the best match with empty candidates."""
        profiles = self.create_test_profiles()
        searcher = FuzzySearcher(profiles)
        
        match, score = searcher.get_best_match("Development", [])
        
        assert match == ""
        assert score == 0