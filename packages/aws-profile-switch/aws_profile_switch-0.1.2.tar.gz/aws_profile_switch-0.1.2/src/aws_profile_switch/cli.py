"""Command-line interface for AWS Profile Switch."""

import sys
from typing import Optional

from .core import AWSProfileSwitcher
from .exceptions import AWSProfileSwitchError
from .shell import ShellDetector


def main() -> None:
    """Main entry point for the CLI application."""
    import argparse
    import os
    import subprocess
    import tempfile
    import sys
    
    parser = argparse.ArgumentParser(description="AWS Profile Switcher")
    parser.add_argument("--exec", action="store_true", 
                       help="Generate a script to source for setting AWS_PROFILE")
    parser.add_argument("--test", action="store_true",
                       help="Test AWS CLI with selected profile")
    parser.add_argument("--info", action="store_true",
                       help="Show usage information")
    parser.add_argument("--quiet", action="store_true",
                       help="Suppress interactive messages (for eval mode)")
    args = parser.parse_args()
    
    # If --info is specified, show usage information
    if args.info:
        print("AWS Profile Switcher Usage:", file=sys.stderr)
        print("", file=sys.stderr)
        print("Basic usage (for eval):", file=sys.stderr)
        print("  eval \"$(aws-profile-switch)\"", file=sys.stderr)
        print("", file=sys.stderr)
        print("Set up alias (recommended):", file=sys.stderr)
        print("  alias aps='eval \"$(aws-profile-switch)\"'", file=sys.stderr)
        print("  aps", file=sys.stderr)
        print("", file=sys.stderr)
        print("Other options:", file=sys.stderr)
        print("  aws-profile-switch --test    # Test selected profile", file=sys.stderr)
        print("  aws-profile-switch --exec    # Generate script to source", file=sys.stderr)
        return
    
    try:
        # For eval mode, suppress output to stderr
        original_stdout = None
        if args.quiet or not (args.exec or args.test or args.info):
            # Redirect stdout to stderr during interaction, then restore for final output
            original_stdout = sys.stdout
            sys.stdout = sys.stderr
        
        switcher = AWSProfileSwitcher()
        selected_profile = switcher.run()
        
        # Restore stdout if we redirected it
        if original_stdout is not None:
            sys.stdout = original_stdout
        
        if selected_profile:
            shell_command = switcher.get_shell_command(selected_profile)
            
            if args.exec:
                # Generate a script to source
                print(f"Setting AWS_PROFILE to: {selected_profile}", file=sys.stderr)
                
                # Create a temporary script to source
                shell = os.environ.get("SHELL", "/bin/bash")
                if "fish" in shell:
                    script_content = f'set -gx AWS_PROFILE "{selected_profile}"\necho "AWS_PROFILE set to: {selected_profile}"\n'
                    temp_ext = ".fish"
                elif "csh" in shell or "tcsh" in shell:
                    script_content = f'setenv AWS_PROFILE "{selected_profile}"\necho "AWS_PROFILE set to: {selected_profile}"\n'
                    temp_ext = ".csh"
                else:
                    script_content = f'export AWS_PROFILE="{selected_profile}"\necho "AWS_PROFILE set to: {selected_profile}"\n'
                    temp_ext = ".sh"
                
                with tempfile.NamedTemporaryFile(mode='w', suffix=temp_ext, delete=False) as f:
                    f.write(script_content)
                    temp_script = f.name
                
                print(f"To apply this setting, run:", file=sys.stderr)
                print(f"source {temp_script}")
                
            elif args.test:
                # Test the profile by running AWS CLI with it
                print(f"Testing profile: {selected_profile}")
                os.environ["AWS_PROFILE"] = selected_profile
                try:
                    result = subprocess.run(["aws", "sts", "get-caller-identity"], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        print("✓ Profile is working correctly!")
                        print(result.stdout)
                    else:
                        print("✗ Profile test failed:")
                        print(result.stderr)
                except subprocess.TimeoutExpired:
                    print("✗ AWS CLI command timed out")
                except FileNotFoundError:
                    print("✗ AWS CLI not found")
                
            else:
                # Output only the shell command for eval execution
                # This is the clean output that eval can execute
                print(shell_command)
        else:
            # User cancelled selection - output a safe no-op command for PowerShell
            shell_detector = ShellDetector()
            shell = shell_detector.detect_shell()
            if shell == "powershell":
                # PowerShell no-op command
                print("# User cancelled selection")
            else:
                # Other shells - just output a comment
                print("# User cancelled selection")
            sys.exit(1)
            
    except AWSProfileSwitchError as e:
        print(f"Error: {e}", file=sys.stderr)
        # Output safe no-op command for PowerShell
        shell_detector = ShellDetector()
        shell = shell_detector.detect_shell()
        if shell == "powershell":
            print("# Error occurred")
        else:
            print("# Error occurred")
        sys.exit(1)
    except KeyboardInterrupt:
        print("", file=sys.stderr)  # Just a newline for cancelled operation
        # Output safe no-op command for PowerShell
        shell_detector = ShellDetector()
        shell = shell_detector.detect_shell()
        if shell == "powershell":
            print("# Operation cancelled")
        else:
            print("# Operation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        # Output safe no-op command for PowerShell
        shell_detector = ShellDetector()
        shell = shell_detector.detect_shell()
        if shell == "powershell":
            print("# Unexpected error occurred")
        else:
            print("# Unexpected error occurred")
        sys.exit(1)


if __name__ == "__main__":
    main()