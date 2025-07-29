"""Tests for CLI interface."""

import pytest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

from aws_profile_switch.cli import main
from aws_profile_switch.exceptions import AWSProfileSwitchError, ConfigFileNotFoundError


class TestCLI:
    """Tests for CLI interface."""
    
    def test_main_successful_selection(self):
        """Test successful profile selection."""
        with patch('aws_profile_switch.cli.AWSProfileSwitcher') as mock_switcher_class:
            mock_switcher = MagicMock()
            mock_switcher_class.return_value = mock_switcher
            mock_switcher.run.return_value = "test-profile"
            mock_switcher.get_shell_command.return_value = 'export AWS_PROFILE="test-profile"'
            
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                
                output = mock_stdout.getvalue()
                assert 'export AWS_PROFILE="test-profile"' in output
                
                mock_switcher.run.assert_called_once()
                mock_switcher.get_shell_command.assert_called_once_with("test-profile")
    
    def test_main_user_cancellation(self):
        """Test user cancelling profile selection."""
        with patch('aws_profile_switch.cli.AWSProfileSwitcher') as mock_switcher_class:
            mock_switcher = MagicMock()
            mock_switcher_class.return_value = mock_switcher
            mock_switcher.run.return_value = None  # User cancelled
            
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 1
            mock_switcher.run.assert_called_once()
            mock_switcher.get_shell_command.assert_not_called()
    
    def test_main_aws_profile_switch_error(self):
        """Test handling of AWSProfileSwitchError."""
        with patch('aws_profile_switch.cli.AWSProfileSwitcher') as mock_switcher_class:
            mock_switcher = MagicMock()
            mock_switcher_class.return_value = mock_switcher
            mock_switcher.run.side_effect = ConfigFileNotFoundError("Config file not found")
            
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                
                assert exc_info.value.code == 1
                stderr_output = mock_stderr.getvalue()
                assert "Error: Config file not found" in stderr_output
    
    def test_main_keyboard_interrupt(self):
        """Test handling of KeyboardInterrupt."""
        with patch('aws_profile_switch.cli.AWSProfileSwitcher') as mock_switcher_class:
            mock_switcher = MagicMock()
            mock_switcher_class.return_value = mock_switcher
            mock_switcher.run.side_effect = KeyboardInterrupt()
            
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                
                assert exc_info.value.code == 1
                stderr_output = mock_stderr.getvalue()
                assert "Operation cancelled by user" in stderr_output
    
    def test_main_unexpected_error(self):
        """Test handling of unexpected errors."""
        with patch('aws_profile_switch.cli.AWSProfileSwitcher') as mock_switcher_class:
            mock_switcher = MagicMock()
            mock_switcher_class.return_value = mock_switcher
            mock_switcher.run.side_effect = Exception("Unexpected error")
            
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                
                assert exc_info.value.code == 1
                stderr_output = mock_stderr.getvalue()
                assert "Unexpected error: Unexpected error" in stderr_output
    
    def test_main_switcher_initialization_error(self):
        """Test handling of errors during switcher initialization."""
        with patch('aws_profile_switch.cli.AWSProfileSwitcher') as mock_switcher_class:
            mock_switcher_class.side_effect = ConfigFileNotFoundError("Config file not found")
            
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                
                assert exc_info.value.code == 1
                stderr_output = mock_stderr.getvalue()
                assert "Error: Config file not found" in stderr_output
    
    def test_main_empty_profile_selection(self):
        """Test handling when profile selection returns empty string."""
        with patch('aws_profile_switch.cli.AWSProfileSwitcher') as mock_switcher_class:
            mock_switcher = MagicMock()
            mock_switcher_class.return_value = mock_switcher
            mock_switcher.run.return_value = ""  # Empty string
            
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 1
            mock_switcher.run.assert_called_once()
            mock_switcher.get_shell_command.assert_not_called()
    
    def test_main_shell_command_generation(self):
        """Test that shell command is generated correctly."""
        with patch('aws_profile_switch.cli.AWSProfileSwitcher') as mock_switcher_class:
            mock_switcher = MagicMock()
            mock_switcher_class.return_value = mock_switcher
            mock_switcher.run.return_value = "my-profile"
            mock_switcher.get_shell_command.return_value = 'export AWS_PROFILE="my-profile"'
            
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                
                output = mock_stdout.getvalue().strip()
                assert output == 'export AWS_PROFILE="my-profile"'
                
                mock_switcher.get_shell_command.assert_called_once_with("my-profile")