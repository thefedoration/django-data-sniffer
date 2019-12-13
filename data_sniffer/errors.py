

class HealthCheckError(Exception):
    """
    Base exception class for anything healthcheck related
    """


class InvalidKeyError(HealthCheckError):
    """
    Thrown if we look up a healthcheck that doesnt exist
    """

class ConfigurationError(HealthCheckError):
    """
    Thrown if we have a configuration that's completely borked
    """

class InvalidAlertError(HealthCheckError):
    """
    Thrown when a query for an alert is invalid
    """
