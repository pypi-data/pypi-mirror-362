import os
import cv2
from .exceptions import FileNotFoundError, FormatNotSupportedError


def validate_input_path(input_path):
    """Validate if input file exists"""
    if not os.path.exists(input_path):
        raise FileNotFoundError(input_path)
    if not os.path.isfile(input_path):
        raise ValueError(f"Input path is not a file: {input_path}")


def get_file_extension(file_path):
    """Get file extension (lowercase, without dot)"""
    return os.path.splitext(file_path)[1].lower().lstrip('.')


def validate_image_format(fmt):
    """Validate if image format is supported"""
    supported = {'jpg', 'jpeg', 'png', 'bmp'}
    if fmt not in supported:
        raise FormatNotSupportedError(f"Image format not supported (supported: {supported})")


def validate_video_format(fmt):
    """Validate if video format is supported"""
    supported = {'mp4', 'avi'}
    if fmt not in supported:
        raise FormatNotSupportedError(f"Video format not supported (supported: {supported})")


def ensure_output_dir(output_path):
    """Ensure output directory exists, create if not"""
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)


def is_directory(path: str) -> bool:
    """
    Check if the given path is a valid directory.

    Args:
        path (str): Path to check

    Returns:
        bool: True if path is a directory, False otherwise
    """
    return os.path.isdir(path)