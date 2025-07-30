# 🌱 NDVI Pro Python SDK (`ndvipy`)

[![PyPI version](https://badge.fury.io/py/ndvipy.svg)](https://badge.fury.io/py/ndvipy)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Professional Python SDK for generating NDVI (Normalized Difference Vegetation Index) visualizations from satellite imagery using the NDVI Pro cloud service.

## 🚀 Quick Start

### Installation

```bash
pip install ndvipy
```

### Basic Usage

```python
from ndvipy import NDVIClient

# Initialize client with your API key
client = NDVIClient(api_key="your_64_character_api_key_here")

# Process an image and save the result
client.save_processed_image("satellite_image.jpg", "ndvi_result.png")

# Or get the result as bytes for further processing
result_bytes = client.process_image("satellite_image.jpg")
with open("ndvi_output.png", "wb") as f:
    f.write(result_bytes)
```

## 🔑 Getting an API Key

1. Sign up at [NDVI Pro Dashboard](https://ndvipro.com/dashboard)
2. Generate your API key in the dashboard
3. All API calls are logged and tracked in your dashboard

## 📖 Documentation

### NDVIClient

The main client class for interacting with the NDVI Pro service.

```python
NDVIClient(
    api_key: str,
    backend_url: str = "https://b563bb24a1b2.ngrok-free.app",
    timeout: int = 120,
    max_retries: int = 3,
    validate_images: bool = True
)
```

**Parameters:**
- `api_key`: Your 64-character API key from the NDVI Pro dashboard
- `backend_url`: Backend service URL (optional, uses default cloud service)
- `timeout`: Request timeout in seconds (default: 120)
- `max_retries`: Maximum retry attempts for failed requests (default: 3)
- `validate_images`: Whether to validate image files before upload (default: True)

### Methods

#### `process_image(image, user_id=None)`

Process an image and return NDVI visualization as PNG bytes.

**Parameters:**
- `image`: Input image. Supports:
  - File path (string or Path object)
  - Raw image bytes
  - Binary file-like object
- `user_id`: Optional user ID for request tracking

**Returns:** PNG image bytes containing the NDVI visualization

**Example:**
```python
# From file path
result = client.process_image("satellite.jpg")

# From bytes
with open("image.jpg", "rb") as f:
    result = client.process_image(f.read())

# From file object
with open("image.jpg", "rb") as f:
    result = client.process_image(f)
```

#### `save_processed_image(image, output_path, user_id=None)`

Process an image and save the result directly to a file.

**Parameters:**
- `image`: Input image (same formats as `process_image`)
- `output_path`: Path where to save the NDVI result
- `user_id`: Optional user ID for request tracking

**Returns:** Path object pointing to the saved file

**Example:**
```python
saved_path = client.save_processed_image("input.jpg", "output.png")
print(f"NDVI result saved to: {saved_path}")
```

#### `validate_api_key()`

Validate that the API key is working correctly.

**Returns:** `True` if API key is valid, `False` otherwise

**Example:**
```python
if client.validate_api_key():
    print("API key is valid!")
else:
    print("Invalid API key")
```

#### `get_health_status()`

Get the health status of the NDVI service.

**Returns:** Dictionary with service health information

**Example:**
```python
health = client.get_health_status()
print(f"Service status: {health['status']}")
```

## 📊 Advanced Examples

### Batch Processing

```python
from ndvipy import NDVIClient
from pathlib import Path

client = NDVIClient(api_key="your_api_key")

# Process all images in a directory
input_dir = Path("satellite_images/")
output_dir = Path("ndvi_results/")
output_dir.mkdir(exist_ok=True)

for image_file in input_dir.glob("*.jpg"):
    try:
        output_file = output_dir / f"ndvi_{image_file.stem}.png"
        client.save_processed_image(image_file, output_file)
        print(f"✅ Processed: {image_file.name}")
    except Exception as e:
        print(f"❌ Failed {image_file.name}: {e}")
```

### Error Handling

```python
from ndvipy import NDVIClient, NDVIError, NDVIAuthError, NDVIValidationError

client = NDVIClient(api_key="your_api_key")

try:
    result = client.process_image("satellite.jpg")
    print("✅ Processing successful!")
    
except NDVIAuthError:
    print("❌ Invalid API key - check your dashboard")
    
except NDVIValidationError as e:
    print(f"❌ Invalid input: {e}")
    
except NDVIError as e:
    print(f"❌ NDVI service error: {e}")
    
except Exception as e:
    print(f"💥 Unexpected error: {e}")
```

### Environment Variable Configuration

```python
import os
from ndvipy import NDVIClient

# Set API key via environment variable
os.environ["NDVI_API_KEY"] = "your_api_key_here"

# Initialize client
api_key = os.getenv("NDVI_API_KEY")
client = NDVIClient(api_key=api_key)
```

### Custom Configuration

```python
from ndvipy import NDVIClient

# Custom configuration for production use
client = NDVIClient(
    api_key="your_api_key",
    timeout=180,  # 3 minute timeout for large images
    max_retries=5,  # More retries for reliability
    validate_images=False  # Skip validation for speed
)
```

## 🔧 Supported Image Formats

- **JPEG** (`.jpg`, `.jpeg`)
- **PNG** (`.png`)
- **TIFF** (`.tiff`, `.tif`)
- **BMP** (`.bmp`)
- **WebP** (`.webp`)

**File Size Limit:** 50MB per image

## ⚡ Performance Tips

1. **Use appropriate timeouts** for your use case
2. **Enable retry logic** for production deployments
3. **Validate images locally** before uploading when possible
4. **Process images in parallel** for batch processing

```python
import concurrent.futures
from ndvipy import NDVIClient

client = NDVIClient(api_key="your_api_key")

def process_single_image(image_path):
    return client.save_processed_image(
        image_path, 
        f"ndvi_{image_path.stem}.png"
    )

# Parallel processing
image_files = ["image1.jpg", "image2.jpg", "image3.jpg"]

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(process_single_image, image_files))
```

## 🛠️ Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=ndvipy
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📝 Error Reference

- **NDVIError**: Base exception for all SDK errors
- **NDVIAuthError**: Invalid API key or authentication failure
- **NDVIValidationError**: Invalid input data or parameters
- **NDVIServerError**: Server-side processing error
- **NDVINetworkError**: Network connection issues
- **NDVITimeoutError**: Request timeout

## 🔗 Links

- [NDVI Pro Dashboard](https://ndvipro.com/dashboard)
- [API Documentation](https://ndvipro.com/docs)
- [GitHub Repository](https://github.com/ndvipro/ndvipy)
- [PyPI Package](https://pypi.org/project/ndvipy/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- 📧 Email: support@ndvipro.com
- 💬 GitHub Issues: [Report a Bug](https://github.com/ndvipro/ndvipy/issues)
- 📖 Documentation: [Full API Docs](https://ndvipro.com/docs)

---

**Built with ❤️ for the remote sensing and agriculture communities** 