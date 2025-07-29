"""Custom exceptions for AWS Profile Switch."""


class AWSProfileSwitchError(Exception):
    """Base exception for AWS Profile Switch errors."""
    pass


class ConfigFileNotFoundError(AWSProfileSwitchError):
    """Raised when the AWS config file is not found."""
    pass


class ConfigParseError(AWSProfileSwitchError):
    """Raised when the AWS config file cannot be parsed."""
    pass


class NoSSOProfilesFoundError(AWSProfileSwitchError):
    """Raised when no SSO profiles are found in the config."""
    pass


class InvalidProfileError(AWSProfileSwitchError):
    """Raised when a profile is missing required SSO fields."""
    pass