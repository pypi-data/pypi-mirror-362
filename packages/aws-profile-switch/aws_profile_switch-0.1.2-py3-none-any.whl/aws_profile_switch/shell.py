"""Shell environment detection and command generation."""

import os
import platform
from typing import Optional


class ShellDetector:
    """Detects the current shell environment and generates appropriate commands."""
    
    @staticmethod
    def detect_shell() -> str:
        """Detect the current shell environment."""
        # Check if we're on Windows
        if platform.system() == "Windows":
            # Check if we're in PowerShell
            if os.environ.get("PSModulePath"):
                return "powershell"
            # Default to cmd on Windows
            return "cmd"
        
        # Unix-like systems
        shell = os.environ.get("SHELL", "")
        if "zsh" in shell:
            return "zsh"
        elif "bash" in shell:
            return "bash"
        elif "fish" in shell:
            return "fish"
        elif "csh" in shell or "tcsh" in shell:
            return "csh"
        else:
            # Default to bash for unknown shells
            return "bash"
    
    @staticmethod
    def generate_export_command(profile_name: str, shell: Optional[str] = None) -> str:
        """Generate the appropriate export command for the detected shell."""
        if shell is None:
            shell = ShellDetector.detect_shell()
        
        if shell == "powershell":
            return f'$env:AWS_PROFILE = "{profile_name}"'
        elif shell == "cmd":
            return f'set AWS_PROFILE={profile_name}'
        elif shell == "fish":
            return f'set -gx AWS_PROFILE "{profile_name}"'
        elif shell in ["csh", "tcsh"]:
            return f'setenv AWS_PROFILE "{profile_name}"'
        else:
            # Default to bash/zsh syntax
            return f'export AWS_PROFILE="{profile_name}"'
    
    @staticmethod
    def generate_unset_command(shell: Optional[str] = None) -> str:
        """Generate the appropriate unset command for the detected shell."""
        if shell is None:
            shell = ShellDetector.detect_shell()
        
        if shell == "powershell":
            return 'Remove-Variable -Name AWS_PROFILE -ErrorAction SilentlyContinue'
        elif shell == "cmd":
            return 'set AWS_PROFILE='
        elif shell == "fish":
            return 'set -e AWS_PROFILE'
        elif shell in ["csh", "tcsh"]:
            return 'unsetenv AWS_PROFILE'
        else:
            # Default to bash/zsh syntax
            return 'unset AWS_PROFILE'