import base64
import io
import uuid
from typing import Optional
from PIL import Image
import numpy as np


def generate_request_id() -> str:
    """Generate a unique request ID."""
    return str(uuid.uuid4())


def image_to_base64(image: Image.Image, format: str = "JPEG") -> str:
    """
    Convert PIL Image to base64 string.
    
    Args:
        image: PIL Image object
        format: Image format (JPEG, PNG, etc.)
    
    Returns:
        Base64 encoded string
    """
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode("utf-8")


def base64_to_image(base64_string: str) -> Image.Image:
    """
    Convert base64 string to PIL Image.
    
    Args:
        base64_string: Base64 encoded image string
    
    Returns:
        PIL Image object
    """
    img_bytes = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(img_bytes))


def base64_to_numpy(base64_string: str) -> np.ndarray:
    """
    Convert base64 string to numpy array (for OpenCV).
    
    Args:
        base64_string: Base64 encoded image string
    
    Returns:
        Numpy array in BGR format (OpenCV compatible)
    """
    image = base64_to_image(base64_string)
    # Convert RGB to BGR for OpenCV
    return np.array(image)[:, :, ::-1]


def numpy_to_base64(image_array: np.ndarray, format: str = "JPEG") -> str:
    """
    Convert numpy array to base64 string.
    
    Args:
        image_array: Numpy array (BGR format from OpenCV)
        format: Image format (JPEG, PNG, etc.)
    
    Returns:
        Base64 encoded string
    """
    # Convert BGR to RGB
    image_rgb = image_array[:, :, ::-1]
    image = Image.fromarray(image_rgb)
    return image_to_base64(image, format)


def validate_image_format(image: Image.Image) -> bool:
    """
    Validate if image format is supported.
    
    Args:
        image: PIL Image object
    
    Returns:
        True if format is supported, False otherwise
    """
    supported_formats = {"JPEG", "PNG", "JPG", "WEBP"}
    return image.format in supported_formats


def resize_image_if_needed(
    image: Image.Image, 
    max_width: int = 1920, 
    max_height: int = 1080
) -> Image.Image:
    """
    Resize image if it exceeds maximum dimensions while maintaining aspect ratio.
    
    Args:
        image: PIL Image object
        max_width: Maximum width
        max_height: Maximum height
    
    Returns:
        Resized PIL Image object
    """
    width, height = image.size
    
    if width <= max_width and height <= max_height:
        return image
    
    # Calculate scaling factor
    width_ratio = max_width / width
    height_ratio = max_height / height
    scale_factor = min(width_ratio, height_ratio)
    
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def calculate_ita_angle(r: int, g: int, b: int) -> float:
    """
    Calculate Individual Typology Angle (ITA°) for skin tone classification.
    
    Args:
        r: Red channel value (0-255)
        g: Green channel value (0-255)
        b: Blue channel value (0-255)
    
    Returns:
        ITA degree value
    """
    import math
    
    # Convert RGB to LAB color space (simplified)
    # This is a simplified version; for production, use proper color space conversion
    l = 0.2126 * r + 0.7152 * g + 0.0722 * b
    a = 1.4749 * (r - l)
    b_val = 0.6721 * (b - l)
    
    # Calculate ITA
    ita = math.degrees(math.atan2(l - 50, b_val))
    return ita


def get_skin_tone_category(ita: float) -> str:
    """
    Categorize skin tone based on ITA° value.
    
    Args:
        ita: ITA degree value
    
    Returns:
        Skin tone category
    """
    if ita > 55:
        return "very_light"
    elif ita > 41:
        return "light"
    elif ita > 28:
        return "intermediate"
    elif ita > 19:
        return "tan"
    elif ita > 10:
        return "brown"
    else:
        return "dark"

