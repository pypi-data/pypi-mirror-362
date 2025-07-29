"""Tests for shell environment detection."""

import os
import pytest
from unittest.mock import patch

from aws_profile_switch.shell import ShellDetector


class TestShellDetector:
    """Tests for ShellDetector class."""
    
    def test_detect_shell_bash(self):
        """Test detecting bash shell."""
        with patch.dict(os.environ, {"SHELL": "/bin/bash"}):
            with patch("platform.system", return_value="Linux"):
                shell = ShellDetector.detect_shell()
                assert shell == "bash"
    
    def test_detect_shell_zsh(self):
        """Test detecting zsh shell."""
        with patch.dict(os.environ, {"SHELL": "/usr/bin/zsh"}):
            with patch("platform.system", return_value="Linux"):
                shell = ShellDetector.detect_shell()
                assert shell == "zsh"
    
    def test_detect_shell_fish(self):
        """Test detecting fish shell."""
        with patch.dict(os.environ, {"SHELL": "/usr/bin/fish"}):
            with patch("platform.system", return_value="Linux"):
                shell = ShellDetector.detect_shell()
                assert shell == "fish"
    
    def test_detect_shell_csh(self):
        """Test detecting csh shell."""
        with patch.dict(os.environ, {"SHELL": "/bin/csh"}):
            with patch("platform.system", return_value="Linux"):
                shell = ShellDetector.detect_shell()
                assert shell == "csh"
    
    def test_detect_shell_tcsh(self):
        """Test detecting tcsh shell."""
        with patch.dict(os.environ, {"SHELL": "/bin/tcsh"}):
            with patch("platform.system", return_value="Linux"):
                shell = ShellDetector.detect_shell()
                assert shell == "csh"
    
    def test_detect_shell_unknown_unix(self):
        """Test detecting unknown Unix shell defaults to bash."""
        with patch.dict(os.environ, {"SHELL": "/bin/unknown"}):
            with patch("platform.system", return_value="Linux"):
                shell = ShellDetector.detect_shell()
                assert shell == "bash"
    
    def test_detect_shell_no_shell_env(self):
        """Test detecting shell with no SHELL environment variable."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("platform.system", return_value="Linux"):
                shell = ShellDetector.detect_shell()
                assert shell == "bash"
    
    def test_detect_shell_powershell(self):
        """Test detecting PowerShell on Windows."""
        with patch.dict(os.environ, {"PSModulePath": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\Modules"}):
            with patch("platform.system", return_value="Windows"):
                shell = ShellDetector.detect_shell()
                assert shell == "powershell"
    
    def test_detect_shell_cmd(self):
        """Test detecting cmd on Windows."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("platform.system", return_value="Windows"):
                shell = ShellDetector.detect_shell()
                assert shell == "cmd"
    
    def test_generate_export_command_bash(self):
        """Test generating export command for bash."""
        command = ShellDetector.generate_export_command("test-profile", "bash")
        assert command == 'export AWS_PROFILE="test-profile"'
    
    def test_generate_export_command_zsh(self):
        """Test generating export command for zsh."""
        command = ShellDetector.generate_export_command("test-profile", "zsh")
        assert command == 'export AWS_PROFILE="test-profile"'
    
    def test_generate_export_command_fish(self):
        """Test generating export command for fish."""
        command = ShellDetector.generate_export_command("test-profile", "fish")
        assert command == 'set -gx AWS_PROFILE "test-profile"'
    
    def test_generate_export_command_csh(self):
        """Test generating export command for csh."""
        command = ShellDetector.generate_export_command("test-profile", "csh")
        assert command == 'setenv AWS_PROFILE "test-profile"'
    
    def test_generate_export_command_tcsh(self):
        """Test generating export command for tcsh."""
        command = ShellDetector.generate_export_command("test-profile", "tcsh")
        assert command == 'setenv AWS_PROFILE "test-profile"'
    
    def test_generate_export_command_powershell(self):
        """Test generating export command for PowerShell."""
        command = ShellDetector.generate_export_command("test-profile", "powershell")
        assert command == '$env:AWS_PROFILE = "test-profile"'
    
    def test_generate_export_command_cmd(self):
        """Test generating export command for cmd."""
        command = ShellDetector.generate_export_command("test-profile", "cmd")
        assert command == 'set AWS_PROFILE=test-profile'
    
    def test_generate_export_command_unknown(self):
        """Test generating export command for unknown shell."""
        command = ShellDetector.generate_export_command("test-profile", "unknown")
        assert command == 'export AWS_PROFILE="test-profile"'
    
    def test_generate_export_command_auto_detect(self):
        """Test generating export command with auto-detection."""
        with patch.dict(os.environ, {"SHELL": "/bin/zsh"}):
            with patch("platform.system", return_value="Linux"):
                command = ShellDetector.generate_export_command("test-profile")
                assert command == 'export AWS_PROFILE="test-profile"'
    
    def test_generate_export_command_special_characters(self):
        """Test generating export command with special characters in profile name."""
        command = ShellDetector.generate_export_command("test-profile-with-special_chars", "bash")
        assert command == 'export AWS_PROFILE="test-profile-with-special_chars"'
    
    def test_generate_unset_command_bash(self):
        """Test generating unset command for bash."""
        command = ShellDetector.generate_unset_command("bash")
        assert command == 'unset AWS_PROFILE'
    
    def test_generate_unset_command_zsh(self):
        """Test generating unset command for zsh."""
        command = ShellDetector.generate_unset_command("zsh")
        assert command == 'unset AWS_PROFILE'
    
    def test_generate_unset_command_fish(self):
        """Test generating unset command for fish."""
        command = ShellDetector.generate_unset_command("fish")
        assert command == 'set -e AWS_PROFILE'
    
    def test_generate_unset_command_csh(self):
        """Test generating unset command for csh."""
        command = ShellDetector.generate_unset_command("csh")
        assert command == 'unsetenv AWS_PROFILE'
    
    def test_generate_unset_command_tcsh(self):
        """Test generating unset command for tcsh."""
        command = ShellDetector.generate_unset_command("tcsh")
        assert command == 'unsetenv AWS_PROFILE'
    
    def test_generate_unset_command_powershell(self):
        """Test generating unset command for PowerShell."""
        command = ShellDetector.generate_unset_command("powershell")
        assert command == 'Remove-Variable -Name AWS_PROFILE -ErrorAction SilentlyContinue'
    
    def test_generate_unset_command_cmd(self):
        """Test generating unset command for cmd."""
        command = ShellDetector.generate_unset_command("cmd")
        assert command == 'set AWS_PROFILE='
    
    def test_generate_unset_command_unknown(self):
        """Test generating unset command for unknown shell."""
        command = ShellDetector.generate_unset_command("unknown")
        assert command == 'unset AWS_PROFILE'
    
    def test_generate_unset_command_auto_detect(self):
        """Test generating unset command with auto-detection."""
        with patch.dict(os.environ, {"SHELL": "/bin/bash"}):
            with patch("platform.system", return_value="Linux"):
                command = ShellDetector.generate_unset_command()
                assert command == 'unset AWS_PROFILE'