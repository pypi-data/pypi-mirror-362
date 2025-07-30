"""
Exception classes for the NDVI Pro Python SDK.
"""


class NDVIError(Exception):
    """Base exception class for all NDVI SDK errors."""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
    
    def __str__(self):
        if self.status_code:
            return f"NDVI Error [{self.status_code}]: {self.message}"
        return f"NDVI Error: {self.message}"


class NDVIAuthError(NDVIError):
    """Raised when API key authentication fails."""
    
    def __init__(self, message: str = "Invalid or missing API key", **kwargs):
        super().__init__(message, **kwargs)


class NDVIServerError(NDVIError):
    """Raised when the NDVI server returns an error."""
    
    def __init__(self, message: str = "Server error occurred", **kwargs):
        super().__init__(message, **kwargs)


class NDVINetworkError(NDVIError):
    """Raised when network connection fails."""
    
    def __init__(self, message: str = "Network connection failed", **kwargs):
        super().__init__(message, **kwargs)


class NDVIValidationError(NDVIError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str = "Input validation failed", **kwargs):
        super().__init__(message, **kwargs)


class NDVITimeoutError(NDVIError):
    """Raised when request times out."""
    
    def __init__(self, message: str = "Request timed out", **kwargs):
        super().__init__(message, **kwargs) 