import os
import cv2
import time
from typing import Optional, Callable
from .core import apply_clahe_enhance
from .utils import (
    validate_input_path, get_file_extension,
    validate_video_format, ensure_output_dir, is_directory
)
from .config import EnhanceConfig
from .exceptions import (
    FileNotFoundError, FormatNotSupportedError, ProcessingError
)

SUPPORTED_VIDEO_FORMATS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}


def enhance_video(
        input_path: str,
        output_path: str,
        output_format: Optional[str] = None,
        config: Optional[EnhanceConfig] = None,
        progress_callback: Optional[Callable[[int], None]] = None
) -> bool:
    """
    Enhance a video file and save the result

    Args:
        input_path (str): Path to input video (supports mp4/avi, etc.)
        output_path (str): Path to save the enhanced video
        output_format (str, optional): Output format (e.g., 'mp4', default inferred from output_path)
        config (EnhanceConfig, optional): Enhancement parameters, default uses default configuration
        progress_callback (Callable[[int], None], optional): Progress callback function, accepts progress percentage (0-100)

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
    validate_video_format(output_format)

    # Ensure output directory exists
    ensure_output_dir(output_path)

    try:
        # Open video file
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise ProcessingError(f"Failed to open video: {input_path}")

        # Get video properties
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if frame_count <= 0:
            raise ProcessingError("Failed to get video frame count")

        # Set encoder based on output format
        fourcc_map = {
            'mp4': 'mp4v',
            'avi': 'XVID',
            'mov': 'avc1',
            'mkv': 'avc1',
            'wmv': 'wmv2'
        }
        if output_format not in fourcc_map:
            raise FormatNotSupportedError(f"Unsupported video format for encoding: {output_format}")
        fourcc = cv2.VideoWriter_fourcc(*fourcc_map[output_format])

        # Create video writer
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        if not out.isOpened():
            raise ProcessingError(f"Failed to create video writer: {output_path}")

        # Process frames
        for frame_idx in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                raise ProcessingError(f"Failed to read video frame (frame {frame_idx})")

            # Apply enhancement
            enhanced_frame = apply_clahe_enhance(frame, config)

            # Write frame
            out.write(enhanced_frame)

            # Update progress (throttle to avoid excessive calls)
            if progress_callback and (frame_idx % 10 == 0 or frame_idx == frame_count - 1):
                progress = min(int((frame_idx + 1) / frame_count * 100), 100)
                progress_callback(progress)

        # Release resources
        cap.release()
        out.release()

        # Final progress update
        if progress_callback:
            progress_callback(100)

        return True

    except Exception as e:
        if isinstance(e, (ProcessingError, FormatNotSupportedError)):
            raise
        raise ProcessingError(f"Video processing failed: {str(e)}")


def enhance_videos_in_folder(
        input_path: str,
        output_path: str,
        output_format: Optional[str] = None,
        config: Optional[EnhanceConfig] = None,
        suffix: str = "_enhanced",
        overwrite: bool = False,
        progress_callback: Optional[Callable[[int, int, int], None]] = None
) -> int:
    """
    Enhance all videos in a folder recursively

    Args:
        input_path (str): Path to input folder
        output_path (str): Path to output folder
        output_format (str, optional): Output format (default uses original format)
        config (EnhanceConfig, optional): Enhancement parameters
        suffix (str): Suffix to append to output filenames
        overwrite (bool): Overwrite existing files if True
        progress_callback (Callable[[int, int, int], None], optional):
            Callback for progress updates (current_video_index, total_videos, current_progress)
            where current_progress is 0-100 for the current video

    Returns:
        int: Number of successfully processed videos

    Raises:
        FileNotFoundError: If input folder does not exist
        ProcessingError: If no supported videos are found in the folder
    """
    # Validate input path is a directory
    if not is_directory(input_path):
        raise FileNotFoundError(f"Input path is not a directory: {input_path}")

    # Configuration setup
    config = config or EnhanceConfig()

    # Ensure output directory exists
    ensure_output_dir(output_path)

    # Collect all supported video files
    video_files = []
    for root, _, files in os.walk(input_path):
        for file in files:
            ext = get_file_extension(file).lower()
            if ext in SUPPORTED_VIDEO_FORMATS:
                video_files.append(os.path.join(root, file))

    if not video_files:
        raise ProcessingError(f"No supported videos found in directory: {input_path}")

    # Process each video
    success_count = 0
    total_videos = len(video_files)

    for video_idx, video_path in enumerate(video_files):
        # Calculate relative path for output
        rel_path = os.path.relpath(video_path, input_path)
        out_dir = os.path.dirname(os.path.join(output_path, rel_path))
        os.makedirs(out_dir, exist_ok=True)

        # Generate output filename
        base_name, ext = os.path.splitext(os.path.basename(video_path))
        out_filename = f"{base_name}{suffix}{ext}" if not output_format else f"{base_name}{suffix}.{output_format}"
        out_file_path = os.path.join(out_dir, out_filename)

        # Skip if file exists and overwrite is False
        if not overwrite and os.path.exists(out_file_path):
            if progress_callback:
                progress_callback(video_idx, total_videos, 100)  # Mark as complete
            continue

        try:
            # Video-specific progress callback
            def video_progress(progress: int):
                if progress_callback:
                    progress_callback(video_idx, total_videos, progress)

            # Enhance the video
            enhance_video(
                input_path=video_path,
                output_path=out_file_path,
                output_format=output_format,
                config=config,
                progress_callback=video_progress
            )
            success_count += 1

        except Exception as e:
            print(f"Skipping {video_path} due to error: {str(e)}")

    return success_count