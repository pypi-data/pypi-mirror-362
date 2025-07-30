import os
from typing import Optional, Callable
import cv2
from .core import apply_clahe_enhance
from .utils import (
    validate_input_path, get_file_extension,
    validate_image_format, ensure_output_dir, is_directory
)
from .config import EnhanceConfig
from .exceptions import (
    FileNotFoundError, FormatNotSupportedError, ProcessingError
)

SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'}


def enhance_image(
        input_path: str,
        output_path: str,
        output_format: Optional[str] = None,
        config: Optional[EnhanceConfig] = None
) -> bool:
    """
    Enhance a single image and save the result

    Args:
        input_path (str): Path to input image (supports jpg/png/bmp, etc.)
        output_path (str): Path to save the enhanced image
        output_format (str, optional): Output format (e.g., 'jpg', default inferred from output_path)
        config (EnhanceConfig, optional): Enhancement parameters, default uses default configuration

    Returns:
        bool: True if processing succeeds

    Raises:
        FileNotFoundError: If input file does not exist
        FormatNotSupportedError: If output format is not supported
        ProcessingError: If an error occurs during processing
    """
    # Configuration setup
    config = config or EnhanceConfig()

    # Validate input path
    validate_input_path(input_path)

    # Determine output format
    if output_format is None:
        output_format = get_file_extension(output_path).lower()
    validate_image_format(output_format)

    # Ensure output directory exists
    ensure_output_dir(output_path)

    try:
        # Read image
        image = cv2.imread(input_path)
        if image is None:
            raise ProcessingError(f"Failed to read image: {input_path}")

        # Apply enhancements
        enhanced_image = apply_clahe_enhance(image, config)

        # Save image with format-specific parameters
        save_params = []
        if output_format in {'jpg', 'jpeg'}:
            save_params = [cv2.IMWRITE_JPEG_QUALITY, 90]
        elif output_format == 'png':
            save_params = [cv2.IMWRITE_PNG_COMPRESSION, 3]

        success = cv2.imwrite(output_path, enhanced_image, save_params)
        if not success:
            raise ProcessingError(f"Failed to save image: {output_path}")

        return True

    except Exception as e:
        if isinstance(e, ProcessingError):
            raise
        raise ProcessingError(f"Image processing failed: {str(e)}")


def enhance_images_in_folder(
        input_path: str,
        output_path: str,
        output_format: Optional[str] = None,
        config: Optional[EnhanceConfig] = None,
        suffix: str = "_enhanced",
        overwrite: bool = False,
        progress_callback: Optional[Callable[[int, int], None]] = None
) -> int:
    """
    Enhance all images in a folder recursively

    Args:
        input_path (str): Path to input folder
        output_path (str): Path to output folder
        output_format (str, optional): Output format (default uses original format)
        config (EnhanceConfig, optional): Enhancement parameters
        suffix (str): Suffix to append to output filenames
        overwrite (bool): Overwrite existing files if True
        progress_callback (Callable[[int, int], None], optional): Callback for progress updates

    Returns:
        int: Number of successfully processed images

    Raises:
        FileNotFoundError: If input folder does not exist
        ProcessingError: If an error occurs during processing
    """
    # Validate input path is a directory
    if not is_directory(input_path):
        raise FileNotFoundError(f"Input path is not a directory: {input_path}")

    # Configuration setup
    config = config or EnhanceConfig()

    # Ensure output directory exists
    ensure_output_dir(output_path)

    # Collect all image files
    image_files = []
    for root, _, files in os.walk(input_path):
        for file in files:
            ext = get_file_extension(file).lower()
            if ext in SUPPORTED_IMAGE_FORMATS:
                image_files.append(os.path.join(root, file))

    if not image_files:
        raise ProcessingError(f"No supported images found in directory: {input_path}")

    # Process each image
    success_count = 0
    for i, img_path in enumerate(image_files):
        # Calculate relative path for output
        rel_path = os.path.relpath(img_path, input_path)
        out_dir = os.path.dirname(os.path.join(output_path, rel_path))
        os.makedirs(out_dir, exist_ok=True)

        # Generate output filename
        base_name, ext = os.path.splitext(os.path.basename(img_path))
        out_filename = f"{base_name}{suffix}{ext}"
        out_file_path = os.path.join(out_dir, out_filename)

        # Skip if file exists and overwrite is False
        if not overwrite and os.path.exists(out_file_path):
            if progress_callback:
                progress_callback(i, len(image_files))
            continue

        try:
            enhance_image(
                input_path=img_path,
                output_path=out_file_path,
                output_format=output_format,
                config=config
            )
            success_count += 1
        except Exception as e:
            print(f"Skipping {img_path} due to error: {str(e)}")

        # Report progress
        if progress_callback:
            progress_callback(i + 1, len(image_files))

    return success_count