

import os
import re
import base64
from pathlib import Path
from typing import Union, Any
import numpy as np


def get_image_data_type(data: Any) -> str:
    """
    Determines the type of image data input.
    
    Args:
        data: Input data that could be various image formats
        
    Returns:
        str: Type of image data ('file_path', 'base64', 'numpy_array', 
            'pil_image', 'opencv_frame', 'bytes', 'url', 'unknown')
    """
    
    # Check if it's a string
    if isinstance(data, str):
        # Check if it's a file path
        if _is_file_path(data):
            return 'file_path'
        
        # Check if it's a URL
        if _is_url(data):
            return 'url'
        
        # Check if it's base64 encoded
        if _is_base64(data):
            return 'base64'
    
    # Check if it's bytes
    elif isinstance(data, bytes):
        return 'bytes'
    
    # Check if it's a numpy array (common for OpenCV frames)
    elif isinstance(data, np.ndarray):
        if len(data.shape) == 2 or (len(data.shape) == 3 and data.shape[2] in [1, 3, 4]):
            return 'numpy_array'
    
    # Check if it's a PIL Image
    elif hasattr(data, 'mode') and hasattr(data, 'size') and hasattr(data, 'format'):
        return 'pil_image'
    
    # Check if it looks like a video frame or OpenCV Mat
    elif hasattr(data, 'shape') and hasattr(data, 'dtype'):
        return 'opencv_frame'
    
    return 'unknown'


def _is_file_path(s: str) -> bool:
    """Check if string is a valid file path."""
    try:
        path = Path(s)
        # Check if it has a common image extension
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp', '.svg'}
        if path.suffix.lower() in image_extensions:
            return True
        # Check if file exists and is a file
        return path.exists() and path.is_file()
    except:
        return False


def _is_url(s: str) -> bool:
    """Check if string is a URL."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(s) is not None


def _is_base64(s: str) -> bool:
    """Check if string is base64 encoded."""
    try:
        # Remove data URL prefix if present
        if s.startswith('data:image/'):
            s = s.split(',', 1)[1]
        
        # Check if it's valid base64
        if len(s) % 4 == 0:
            base64.b64decode(s, validate=True)
            return True
    except:
        pass
    return False
