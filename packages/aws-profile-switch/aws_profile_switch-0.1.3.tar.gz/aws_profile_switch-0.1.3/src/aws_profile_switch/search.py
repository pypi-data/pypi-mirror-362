"""Fuzzy search functionality for AWS profiles."""

from typing import List, Tuple
from fuzzywuzzy import fuzz, process

from .models import SSOProfile


class FuzzySearcher:
    """Provides fuzzy search capabilities for AWS profiles."""
    
    def __init__(self, profiles: List[SSOProfile]):
        """Initialize the fuzzy searcher with a list of profiles."""
        self.profiles = profiles
    
    def search_accounts(self, query: str, limit: int = 10) -> List[str]:
        """Search for account names matching the query."""
        if not query.strip():
            return []
        
        # Get unique account names
        account_names = list(set(profile.sso_account_name for profile in self.profiles))
        
        # Perform fuzzy search
        matches = process.extract(
            query,
            account_names,
            scorer=fuzz.WRatio,
            limit=limit
        )
        
        # Return account names sorted by match score (descending)
        return [match[0] for match in matches if match[1] > 30]  # Minimum 30% match
    
    def search_roles(self, query: str, account_name: str, limit: int = 10) -> List[str]:
        """Search for role names matching the query within a specific account."""
        if not query.strip():
            return []
        
        # Get roles for the specific account
        roles = [
            profile.sso_role_name
            for profile in self.profiles
            if profile.sso_account_name == account_name
        ]
        
        # Remove duplicates
        unique_roles = list(set(roles))
        
        # Perform fuzzy search
        matches = process.extract(
            query,
            unique_roles,
            scorer=fuzz.WRatio,
            limit=limit
        )
        
        # Return role names sorted by match score (descending)
        return [match[0] for match in matches if match[1] > 30]  # Minimum 30% match
    
    def search_profiles(self, query: str, limit: int = 10) -> List[SSOProfile]:
        """Search for profiles matching the query across all fields."""
        if not query.strip():
            return []
        
        # Create searchable strings for each profile
        profile_strings = []
        for profile in self.profiles:
            search_string = f"{profile.sso_account_name} {profile.sso_role_name} {profile.profile_name}"
            profile_strings.append(search_string)
        
        # Perform fuzzy search
        matches = process.extract(
            query,
            profile_strings,
            scorer=fuzz.WRatio,
            limit=limit
        )
        
        # Return profiles sorted by match score (descending)
        result = []
        for match in matches:
            if match[1] > 30:  # Minimum 30% match
                # Find the original profile by index
                index = profile_strings.index(match[0])
                result.append(self.profiles[index])
        
        return result
    
    def get_best_match(self, query: str, candidates: List[str]) -> Tuple[str, int]:
        """Get the best matching candidate for a query."""
        if not query.strip() or not candidates:
            return "", 0
        
        match = process.extractOne(
            query,
            candidates,
            scorer=fuzz.WRatio
        )
        
        return match if match else ("", 0)