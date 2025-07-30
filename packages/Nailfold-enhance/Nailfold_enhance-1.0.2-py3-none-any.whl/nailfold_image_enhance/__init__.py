# Expose core API
from .image_processor import enhance_image, enhance_images_in_folder
from .video_processor import enhance_video, enhance_videos_in_folder
from .config import EnhanceConfig

# Expose exception classes
from .exceptions import (
    MedicalEnhanceError,
    FileNotFoundError,
    FormatNotSupportedError,
    ProcessingError
)

# Version information
__version__ = "1.0.0"
