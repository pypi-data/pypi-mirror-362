"""User interface components using prompt_toolkit."""

from typing import List, Optional, Callable, Any
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import radiolist_dialog, message_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.application import Application
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea, Frame, Label
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.keys import Keys

from .models import SSOProfile
from .search import FuzzySearcher


class ProfileCompleter(Completer):
    """Custom completer for profile selection."""
    
    def __init__(self, get_completions_func: Callable[[str], List[str]]):
        """Initialize with a function that provides completions."""
        self.get_completions_func = get_completions_func
    
    def get_completions(self, document, complete_event):
        """Get completions for the current document."""
        word = document.get_word_before_cursor()
        completions = self.get_completions_func(word)
        
        for completion in completions:
            yield Completion(completion, start_position=-len(word))



class InlineProfileSelector:
    """Inline profile selector that doesn't use modal dialogs."""
    
    def __init__(self, profiles: List[SSOProfile]):
        """Initialize the profile selector."""
        self.profiles = profiles
        self.searcher = FuzzySearcher(profiles)
    
    def select_from_recent(self, recent_profiles: List[str]) -> Optional[str]:
        """Select from recent profiles using inline completion."""
        if not recent_profiles:
            return None
            
        # Filter recent profiles to only include valid ones
        valid_recent = []
        for profile_name in recent_profiles:
            profile = next((p for p in self.profiles if p.profile_name == profile_name), None)
            if profile:
                valid_recent.append(profile_name)
        
        if not valid_recent:
            return None
        
        # Create completer that prioritizes recent profiles
        def get_completions(query: str) -> List[str]:
            if not query.strip():
                return valid_recent
            
            # Search in recent profiles first
            recent_matches = [p for p in valid_recent if query.lower() in p.lower()]
            if recent_matches:
                return recent_matches
            
            # Fall back to general search
            profile_matches = self.searcher.search_profiles(query)
            return [p.profile_name for p in profile_matches[:10]]
        
        completer = ProfileCompleter(get_completions)
        
        try:
            print("Recent profiles available:")
            for i, profile_name in enumerate(valid_recent[:5], 1):
                profile = next(p for p in self.profiles if p.profile_name == profile_name)
                print(f"  {i}. {profile_name} ({profile.display_name})")
            
            print("\nType profile name or part of it (Tab for completion):")
            
            result = prompt(
                "Profile: ",
                completer=completer,
                complete_while_typing=True,
                default=""
            ).strip()
            
            if not result:
                return None
            
            # Check if result is a valid profile name
            if result in [p.profile_name for p in self.profiles]:
                return result
            
            # Try to find best match
            all_profiles = [p.profile_name for p in self.profiles]
            best_match, score = self.searcher.get_best_match(result, all_profiles)
            
            if score > 70:
                return best_match
            
            return None
            
        except (KeyboardInterrupt, EOFError):
            return None


class ProfileSelector:
    """Interactive profile selector using prompt_toolkit."""
    
    def __init__(self, profiles: List[SSOProfile]):
        """Initialize the profile selector."""
        self.profiles = profiles
        self.searcher = FuzzySearcher(profiles)
        self.inline_selector = InlineProfileSelector(profiles)
        
        # Define UI style
        self.style = Style.from_dict({
            'dialog': 'bg:#4444aa',
            'dialog.body': 'bg:#ffffff #000000',
            'dialog.body label': 'bg:#ffffff #000000',
            'dialog.body text': 'bg:#ffffff #000000',
            'dialog.body radiolist': 'bg:#ffffff #000000',
            'dialog shadow': 'bg:#000000',
            'radiolist': 'bg:#ffffff #000000',
            'radiolist.selected': 'bg:#4444aa #ffffff',
            'radiolist.focused': 'bg:#4444aa #ffffff',
            'button': 'bg:#4444aa #ffffff',
            'button.focused': 'bg:#ffffff #000000',
        })
    
    def show_recent_profiles(self, recent_profiles: List[str]) -> Optional[str]:
        """Show recent profiles inline."""
        return self.inline_selector.select_from_recent(recent_profiles)
    
    def search_accounts_with_history(self, recent_profiles: List[str]) -> Optional[str]:
        """Interactive account search with history support via arrow keys."""
        if not recent_profiles:
            return self.search_accounts()
        
        # Limit to 5 recent profiles and get their account names
        valid_recent = []
        for profile_name in recent_profiles[:5]:
            profile = next((p for p in self.profiles if p.profile_name == profile_name), None)
            if profile:
                valid_recent.append((profile_name, profile.sso_account_name))
        
        if not valid_recent:
            return self.search_accounts()
        
        current_index = -1  # -1 means no selection from history
        
        # Set up key bindings for arrow key detection
        bindings = KeyBindings()
        
        @bindings.add(Keys.Up)
        def _(event):
            nonlocal current_index
            if current_index < len(valid_recent) - 1:
                current_index += 1
                profile_name, account_name = valid_recent[current_index]
                event.app.current_buffer.text = account_name
                event.app.current_buffer.cursor_position = len(account_name)
        
        @bindings.add(Keys.Down)
        def _(event):
            nonlocal current_index
            if current_index > 0:
                current_index -= 1
                profile_name, account_name = valid_recent[current_index]
                event.app.current_buffer.text = account_name
                event.app.current_buffer.cursor_position = len(account_name)
            elif current_index == 0:
                current_index = -1
                event.app.current_buffer.text = ""
                event.app.current_buffer.cursor_position = 0
        
        # Create a simple completer for account names
        def get_account_completions(query: str) -> List[str]:
            if not query.strip():
                return []
            
            all_accounts = sorted(list(set(profile.sso_account_name for profile in self.profiles)))
            query_lower = query.lower()
            
            # Filter accounts that contain the query (case-insensitive)
            matching_accounts = [
                acc for acc in all_accounts 
                if query_lower in acc.lower()
            ]
            
            # If we have exact substring matches, prefer them
            if matching_accounts:
                return matching_accounts[:10]
            
            # Otherwise, fall back to fuzzy search
            return self.searcher.search_accounts(query)[:10]
        
        completer = ProfileCompleter(get_account_completions)
        
        try:
            print("Type account name (or use ↑↓ for recent profiles):")
            if valid_recent:
                print("Recent profiles:")
                for i, (profile_name, account_name) in enumerate(valid_recent):
                    print(f"  {account_name} (from {profile_name})")
            
            result = prompt(
                "Account: ",
                completer=completer,
                complete_while_typing=True,
                key_bindings=bindings,
                default=""
            ).strip()
            
            if not result:
                return None
            
            # Check if result is a valid account name
            all_accounts_set = set(profile.sso_account_name for profile in self.profiles)
            if result in all_accounts_set:
                return result
            
            # Try to find the best match
            best_match, score = self.searcher.get_best_match(result, list(all_accounts_set))
            if score > 70:  # High confidence match
                print(f"Using best match: {best_match}")
                return best_match
            
            # Show available matches
            matches = self.searcher.search_accounts(result)
            if matches:
                print(f"No exact match found. Similar accounts:")
                for i, match in enumerate(matches[:5], 1):
                    print(f"  {i}. {match}")
                
                try:
                    choice = prompt("Select number or type account name: ").strip()
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(matches):
                            return matches[idx]
                    elif choice:
                        # Try the typed input again
                        best_match, score = self.searcher.get_best_match(choice, matches)
                        if score > 50:
                            return best_match
                except (KeyboardInterrupt, EOFError):
                    return None
            
            print(f"No accounts found matching '{result}'.")
            return None
            
        except (KeyboardInterrupt, EOFError):
            return None

    def search_accounts(self, initial_query: str = "") -> Optional[str]:
        """Interactive account search."""
        def get_account_completions(query: str) -> List[str]:
            if not query.strip():
                # Don't show any completions when no query is entered
                return []
            
            all_accounts = sorted(list(set(profile.sso_account_name for profile in self.profiles)))
            query_lower = query.lower()
            
            # Filter accounts that contain the query (case-insensitive)
            matching_accounts = [
                acc for acc in all_accounts 
                if query_lower in acc.lower()
            ]
            
            # If we have exact substring matches, prefer them
            if matching_accounts:
                return matching_accounts[:10]
            
            # Otherwise, fall back to fuzzy search
            return self.searcher.search_accounts(query)[:10]
        
        completer = ProfileCompleter(get_account_completions)
        
        try:
            # Show available accounts
            all_accounts = sorted(list(set(profile.sso_account_name for profile in self.profiles)))
            print("Available accounts:")
            for i, account in enumerate(all_accounts[:10], 1):
                print(f"  {i}. {account}")
            if len(all_accounts) > 10:
                print(f"  ... and {len(all_accounts) - 10} more")
            
            print("\nType account name or part of it (Tab for completion):")
            
            account_name = prompt(
                "Account: ",
                completer=completer,
                complete_while_typing=True,
                default=initial_query
            ).strip()
            
            if not account_name:
                return None
            
            # Check if the entered account name is valid
            all_accounts_set = set(profile.sso_account_name for profile in self.profiles)
            if account_name in all_accounts_set:
                return account_name
            
            # Try to find the best match
            best_match, score = self.searcher.get_best_match(account_name, list(all_accounts_set))
            if score > 70:  # High confidence match
                print(f"Using best match: {best_match}")
                return best_match
            
            # Show available matches
            matches = self.searcher.search_accounts(account_name)
            if matches:
                print(f"No exact match found. Similar accounts:")
                for i, match in enumerate(matches[:5], 1):
                    print(f"  {i}. {match}")
                
                try:
                    choice = prompt("Select number or type account name: ").strip()
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(matches):
                            return matches[idx]
                    elif choice:
                        # Try the typed input again
                        best_match, score = self.searcher.get_best_match(choice, matches)
                        if score > 50:
                            return best_match
                except (KeyboardInterrupt, EOFError):
                    return None
            
            print(f"No accounts found matching '{account_name}'.")
            return None
            
        except (KeyboardInterrupt, EOFError):
            return None
    
    def search_roles(self, account_name: str, initial_query: str = "") -> Optional[str]:
        """Interactive role search for a specific account."""
        def get_role_completions(query: str) -> List[str]:
            if not query.strip():
                # Don't show any completions when no query is entered
                return []
            
            # Get all roles for this account
            available_roles = sorted(list(set([
                profile.sso_role_name
                for profile in self.profiles
                if profile.sso_account_name == account_name
            ])))
            
            # Filter roles that contain the query (case-insensitive)
            query_lower = query.lower()
            matching_roles = [
                role for role in available_roles 
                if query_lower in role.lower()
            ]
            
            # If we have exact substring matches, prefer them
            if matching_roles:
                return matching_roles[:10]
            
            # Otherwise, fall back to fuzzy search
            return self.searcher.search_roles(query, account_name)
        
        completer = ProfileCompleter(get_role_completions)
        
        try:
            # Show available roles for this account
            available_roles = sorted(list(set([
                profile.sso_role_name
                for profile in self.profiles
                if profile.sso_account_name == account_name
            ])))
            
            print(f"Available roles for '{account_name}':")
            for i, role in enumerate(available_roles, 1):
                print(f"  {i}. {role}")
            
            print("\nType role name or part of it (Tab for completion):")
            
            role_name = prompt(
                "Role: ",
                completer=completer,
                complete_while_typing=True,
                default=initial_query
            ).strip()
            
            if not role_name:
                return None
            
            # Check if the entered role name is valid for this account
            if role_name in available_roles:
                return role_name
            
            # Try to find the best match
            best_match, score = self.searcher.get_best_match(role_name, available_roles)
            if score > 70:  # High confidence match
                print(f"Using best match: {best_match}")
                return best_match
            
            # Show available matches
            matches = self.searcher.search_roles(role_name, account_name)
            if matches:
                print(f"No exact match found. Similar roles:")
                for i, match in enumerate(matches, 1):
                    print(f"  {i}. {match}")
                
                try:
                    choice = prompt("Select number or type role name: ").strip()
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(matches):
                            return matches[idx]
                    elif choice:
                        # Try the typed input again
                        best_match, score = self.searcher.get_best_match(choice, matches)
                        if score > 50:
                            return best_match
                except (KeyboardInterrupt, EOFError):
                    return None
            
            print(f"No roles found matching '{role_name}' for account '{account_name}'.")
            return None
            
        except (KeyboardInterrupt, EOFError):
            return None
    
    def select_profile(self, account_name: str, role_name: str) -> Optional[str]:
        """Select a profile from matching account and role."""
        matching_profiles = [
            profile for profile in self.profiles
            if profile.sso_account_name == account_name and profile.sso_role_name == role_name
        ]
        
        if not matching_profiles:
            return None
        
        if len(matching_profiles) == 1:
            return matching_profiles[0].profile_name
        
        # Multiple profiles match, let user choose
        print(f"Multiple profiles found for {account_name} - {role_name}:")
        for i, profile in enumerate(matching_profiles, 1):
            print(f"  {i}. {profile.profile_name} (Account ID: {profile.sso_account_id})")
        
        try:
            choice = prompt("Select number: ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(matching_profiles):
                    return matching_profiles[idx].profile_name
            
            return None
            
        except (KeyboardInterrupt, EOFError):
            return None