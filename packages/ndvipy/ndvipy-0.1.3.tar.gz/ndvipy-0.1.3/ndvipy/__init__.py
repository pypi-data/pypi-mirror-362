"""
NDVI Pro Python SDK
===================

A robust Python client for the NDVI Pro cloud service.
Generate vegetation analysis from satellite imagery with just a few lines of code.

Quick Start
-----------
```python
from ndvipy import NDVIClient

# Initialize client with your API key
client = NDVIClient(api_key="your_64_char_api_key_here")

# Process an image
result_bytes = client.process_image("satellite_image.jpg")

# Save the result
with open("ndvi_result.png", "wb") as f:
    f.write(result_bytes)

# Or use the shortcut method
client.save_processed_image("input.jpg", "output.png")
```

Features
--------
- Simple, intuitive API
- Automatic error handling and retries
- Support for multiple image formats
- Comprehensive logging and debugging
- Usage tracking in your NDVI Pro dashboard

License
-------
MIT License
"""

from .client import NDVIClient
from .exceptions import (
    NDVIError, 
    NDVIAuthError, 
    NDVIServerError, 
    NDVINetworkError,
    NDVIValidationError,
    NDVITimeoutError
)

__version__ = "0.1.2"
__all__ = [
    "NDVIClient", 
    "NDVIError", 
    "NDVIAuthError", 
    "NDVIServerError", 
    "NDVINetworkError",
    "NDVIValidationError",
    "NDVITimeoutError"
] 