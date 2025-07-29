class APIError(Exception):
    """Base class for all API exceptions."""
    pass

class AuthenticationError(APIError):
    """Raised when authentication fails."""
    pass

class RateLimitError(APIError):
    """Raised when the API rate limit is exceeded."""
    pass

class ConnectionError(APIError):
    """Raised when a connection error occurs."""
    pass

class BadRequestError(APIError):
    """Raised when bad request error occurs."""
    pass

class ServiceAppError(APIError):
    """Service Application Client exception"""
    pass

class DirectoryClientError(APIError):
    """Directory Application Client exception"""
    pass

class DiskClientError(APIError):
    """Disk Application Client exception"""
    pass

class MailAuditError(APIError):
    """Mail Audit Log exception"""
    pass

class EventAuditError(APIError):
    """Event Audit Log exception"""
    pass