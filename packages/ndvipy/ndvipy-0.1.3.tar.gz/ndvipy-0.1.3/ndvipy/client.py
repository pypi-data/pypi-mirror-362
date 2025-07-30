"""
NDVI Pro Python SDK Client
"""

from __future__ import annotations

import io
import logging
import mimetypes
import time
from pathlib import Path
from typing import Union, BinaryIO, Optional, Dict, Any

import requests
from PIL import Image

from .exceptions import (
    NDVIError,
    NDVIAuthError,
    NDVIServerError,
    NDVINetworkError,
    NDVIValidationError,
    NDVITimeoutError,
)

# Configure logging
logger = logging.getLogger(__name__)

# Default configuration
# Production backend hosted on Railway
DEFAULT_BACKEND_URL = "https://server-production-907e.up.railway.app"
DEFAULT_TIMEOUT = 120  # 2 minutes for image processing
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.webp'}


class NDVIClient:
    """
    Professional client for the NDVI Pro cloud service.
    
    This client provides a simple interface to process satellite imagery
    and generate NDVI (Normalized Difference Vegetation Index) visualizations
    using machine learning models in the cloud.
    
    Features:
        - Automatic API key validation
        - Comprehensive error handling
        - Support for multiple image formats
        - Request retry logic
        - Usage tracking and logging
        - Input validation and sanitization
    
    Example:
        >>> from ndvipy import NDVIClient
        >>> client = NDVIClient(api_key="your_api_key_here")
        >>> result = client.process_image("satellite.jpg")
        >>> client.save_processed_image("input.jpg", "output.png")
    
    Args:
        api_key: Your 64-character API key from NDVI Pro dashboard
        backend_url: Backend service URL (optional)
        timeout: Request timeout in seconds (default: 120)
        max_retries: Maximum retry attempts for failed requests (default: 3)
        validate_images: Whether to validate image files before upload (default: True)
    """

    def __init__(
        self,
        api_key: str,
        *,
        backend_url: str = DEFAULT_BACKEND_URL,
        timeout: Union[int, float] = DEFAULT_TIMEOUT,
        max_retries: int = 3,
        validate_images: bool = True,
    ):
        # Validate API key
        if not api_key:
            raise NDVIValidationError("API key is required")
        if not isinstance(api_key, str):
            raise NDVIValidationError("API key must be a string")
        if len(api_key) < 32:
            raise NDVIValidationError(
                "API key appears invalid - expected at least 32 characters. "
                "Please check your API key from the NDVI Pro dashboard."
            )

        self.api_key = api_key.strip()
        self.backend_url = backend_url.rstrip("/")
        self.timeout = max(30, timeout)  # Minimum 30 seconds
        self.max_retries = max(0, max_retries)
        self.validate_images = validate_images

        # Create HTTP session with default headers
        self._session = requests.Session()
        self._session.headers.update({
            "X-API-Key": self.api_key,
            "ngrok-skip-browser-warning": "true",
            "User-Agent": f"ndvipy/0.1.2 (Python {self._get_python_version()})",
        })

        logger.info(f"Initialized NDVI client with backend: {self.backend_url}")

    def process_image(
        self, 
        image: Union[str, Path, bytes, BinaryIO], 
        user_id: Optional[str] = None
    ) -> bytes:
        """
        Process an image and return NDVI visualization as PNG bytes.
        
        This method sends your image to the NDVI Pro cloud service for processing.
        The request will be logged and appear in your dashboard usage statistics.
        
        Args:
            image: Image to process. Can be:
                - Path to local image file (str or Path)
                - Raw image bytes
                - Binary file-like object
            user_id: Optional user ID for request tracking
        
        Returns:
            PNG image bytes containing the NDVI visualization
        
        Raises:
            NDVIValidationError: Invalid image format or size
            NDVIAuthError: Invalid API key
            NDVIServerError: Server processing error
            NDVINetworkError: Network connection failed
            NDVITimeoutError: Request timed out
        
        Example:
            >>> result_bytes = client.process_image("satellite.jpg")
            >>> with open("ndvi_output.png", "wb") as f:
            ...     f.write(result_bytes)
        """
        # Validate and prepare image data
        image_data, filename, content_type = self._prepare_image(image)
        
        # Prepare request
        files = {"image": (filename, image_data, content_type)}
        headers = {}
        if user_id:
            headers["X-User-Id"] = str(user_id)
        
        url = f"{self.backend_url}/process-ndvi"
        
        # Execute request with retries
        return self._execute_request_with_retries(
            method="POST",
            url=url,
            files=files,
            headers=headers,
            operation="process_image"
        )

    def save_processed_image(
        self, 
        image: Union[str, Path, bytes, BinaryIO], 
        output_path: Union[str, Path],
        user_id: Optional[str] = None
    ) -> Path:
        """
        Process an image and save the result directly to a file.
        
        Args:
            image: Input image (same formats as process_image)
            output_path: Path where to save the NDVI result
            user_id: Optional user ID for request tracking
        
        Returns:
            Path object pointing to the saved file
        
        Example:
            >>> saved_path = client.save_processed_image("input.jpg", "output.png")
            >>> print(f"NDVI result saved to: {saved_path}")
        """
        output_path = Path(output_path).expanduser().resolve()
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Process image and save result
        result_bytes = self.process_image(image, user_id=user_id)
        output_path.write_bytes(result_bytes)
        
        logger.info(f"Saved NDVI result to: {output_path}")
        return output_path

    def validate_api_key(self) -> bool:
        """
        Validate that the API key is working correctly.
        
        Returns:
            True if API key is valid, False otherwise
        
        Example:
            >>> if client.validate_api_key():
            ...     print("API key is valid!")
        """
        try:
            url = f"{self.backend_url}/validate-key"
            response = self._session.get(url, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False

    def get_health_status(self) -> Dict[str, Any]:
        """
        Get the health status of the NDVI service.
        
        Returns:
            Dictionary with service health information
        
        Raises:
            NDVINetworkError: If unable to connect to service
        """
        try:
            url = f"{self.backend_url}/health"
            response = self._session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise NDVINetworkError(f"Unable to check service health: {e}")

    # -------------------------------------------------------------------------
    # Private methods
    # -------------------------------------------------------------------------

    def _prepare_image(self, image: Union[str, Path, bytes, BinaryIO]) -> tuple:
        """Validate and prepare image data for upload."""
        if isinstance(image, (str, Path)):
            return self._prepare_file_image(Path(image))
        elif isinstance(image, bytes):
            return self._prepare_bytes_image(image)
        elif hasattr(image, 'read'):
            return self._prepare_stream_image(image)
        else:
            raise NDVIValidationError(
                "Unsupported image type. Expected file path, bytes, or file-like object."
            )

    def _prepare_file_image(self, image_path: Path) -> tuple:
        """Prepare image from file path."""
        image_path = image_path.expanduser().resolve()
        
        if not image_path.exists():
            raise NDVIValidationError(f"Image file not found: {image_path}")
        
        if not image_path.is_file():
            raise NDVIValidationError(f"Path is not a file: {image_path}")
        
        # Check file size
        file_size = image_path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            raise NDVIValidationError(
                f"Image file too large: {file_size / 1024 / 1024:.1f}MB "
                f"(max: {MAX_FILE_SIZE / 1024 / 1024:.0f}MB)"
            )
        
        # Check file extension
        if self.validate_images and image_path.suffix.lower() not in SUPPORTED_FORMATS:
            raise NDVIValidationError(
                f"Unsupported image format: {image_path.suffix}. "
                f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
            )
        
        # Validate image can be opened (if validation enabled)
        if self.validate_images:
            try:
                with Image.open(image_path) as img:
                    img.verify()
            except Exception as e:
                raise NDVIValidationError(f"Invalid or corrupted image file: {e}")
        
        image_data = image_path.read_bytes()
        content_type = mimetypes.guess_type(str(image_path))[0] or "image/jpeg"
        
        return image_data, image_path.name, content_type

    def _prepare_bytes_image(self, image_bytes: bytes) -> tuple:
        """Prepare image from bytes."""
        if len(image_bytes) == 0:
            raise NDVIValidationError("Empty image data provided")
        
        if len(image_bytes) > MAX_FILE_SIZE:
            raise NDVIValidationError(
                f"Image data too large: {len(image_bytes) / 1024 / 1024:.1f}MB "
                f"(max: {MAX_FILE_SIZE / 1024 / 1024:.0f}MB)"
            )
        
        # Validate image format if validation enabled
        if self.validate_images:
            try:
                with Image.open(io.BytesIO(image_bytes)) as img:
                    img.verify()
            except Exception as e:
                raise NDVIValidationError(f"Invalid image data: {e}")
        
        return image_bytes, "image.jpg", "image/jpeg"

    def _prepare_stream_image(self, image_stream: BinaryIO) -> tuple:
        """Prepare image from file-like object."""
        try:
            image_data = image_stream.read()
            return self._prepare_bytes_image(image_data)
        except Exception as e:
            raise NDVIValidationError(f"Failed to read image stream: {e}")

    def _execute_request_with_retries(
        self, 
        method: str, 
        url: str, 
        operation: str,
        **kwargs
    ) -> bytes:
        """Execute HTTP request with retry logic."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    wait_time = min(2 ** attempt, 10)  # Exponential backoff, max 10s
                    logger.info(f"Retrying {operation} (attempt {attempt + 1}) in {wait_time}s...")
                    time.sleep(wait_time)
                
                response = self._session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )
                
                return self._handle_response(response, operation)
                
            except requests.exceptions.Timeout as e:
                last_exception = NDVITimeoutError(
                    f"Request timed out after {self.timeout} seconds"
                )
                logger.warning(f"Timeout on attempt {attempt + 1}: {e}")
                
            except requests.exceptions.ConnectionError as e:
                last_exception = NDVINetworkError(
                    f"Network connection failed: {e}"
                )
                logger.warning(f"Connection error on attempt {attempt + 1}: {e}")
                
            except requests.exceptions.RequestException as e:
                last_exception = NDVINetworkError(f"Request failed: {e}")
                logger.warning(f"Request error on attempt {attempt + 1}: {e}")
                
            except NDVIError:
                # Don't retry on API errors (auth, validation, etc.)
                raise
        
        # All retries exhausted
        raise last_exception

    def _handle_response(self, response: requests.Response, operation: str) -> bytes:
        """Handle and validate HTTP response."""
        logger.debug(f"Response status: {response.status_code} for {operation}")
        
        if response.status_code == 401:
            raise NDVIAuthError(
                "Invalid API key. Please check your API key from the NDVI Pro dashboard.",
                status_code=response.status_code
            )
        
        elif response.status_code == 400:
            try:
                error_data = response.json()
                error_msg = error_data.get("error", "Bad request")
            except:
                error_msg = "Invalid request parameters"
            raise NDVIValidationError(error_msg, status_code=response.status_code)
        
        elif response.status_code == 429:
            raise NDVIServerError(
                "Rate limit exceeded. Please wait before making more requests.",
                status_code=response.status_code
            )
        
        elif response.status_code >= 500:
            try:
                error_data = response.json()
                error_msg = error_data.get("error", "Server error")
            except:
                error_msg = f"Server error ({response.status_code})"
            raise NDVIServerError(error_msg, status_code=response.status_code)
        
        elif not response.ok:
            raise NDVIServerError(
                f"Unexpected error ({response.status_code})",
                status_code=response.status_code
            )
        
        # Check response content type
        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            # Might be JSON error response
            try:
                error_data = response.json()
                error_msg = error_data.get("error", "Unexpected response format")
                raise NDVIServerError(error_msg, response_data=error_data)
            except:
                raise NDVIServerError("Unexpected response format")
        
        # Validate response size
        content_length = len(response.content)
        if content_length == 0:
            raise NDVIServerError("Empty response received")
        
        logger.info(f"Successfully processed image, received {content_length} bytes")
        return response.content

    @staticmethod
    def _get_python_version() -> str:
        """Get Python version string."""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}" 