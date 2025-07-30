import os
import cv2
import numpy as np

from .exceptions import FileNotFoundError, FormatNotSupportedError

SUPPORTED_IMAGE_FORMATS = {'jpg', 'jpeg', 'png', 'bmp', 'tif', 'tiff'}
SUPPORTED_VIDEO_FORMATS = {'mp4', 'avi', 'mov', 'mkv'}

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


def is_supported_image(path: str) -> bool:
    """检查文件是否为支持的图像格式（处理中文路径）"""
    try:
        ext = os.path.splitext(path)[1].lower().lstrip('.')  # 移除点并转小写
        return ext in SUPPORTED_IMAGE_FORMATS
    except Exception:
        return False


def is_supported_video(path: str) -> bool:
    """检查文件是否为支持的视频格式（处理中文路径）"""
    try:
        ext = os.path.splitext(path)[1].lower().lstrip('.')  # 移除点并转小写
        return ext in SUPPORTED_VIDEO_FORMATS
    except Exception:
        return False


def read_image(path: str) -> np.ndarray:
    """读取图像（支持中文路径）"""
    try:
        # OpenCV默认不支持中文路径，使用字节读取
        with open(path, 'rb') as f:
            img_array = np.asarray(bytearray(f.read()), dtype=np.uint8)
        return cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    except Exception as e:
        raise ValueError(f"无法读取图像: {str(e)}")


def save_image(path: str, image: np.ndarray) -> None:
    """保存图像（支持中文路径）"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # 使用字节写入
        _, buffer = cv2.imencode(os.path.splitext(path)[1], image)
        with open(path, 'wb') as f:
            f.write(buffer)
    except Exception as e:
        raise ValueError(f"无法保存图像: {str(e)}")
