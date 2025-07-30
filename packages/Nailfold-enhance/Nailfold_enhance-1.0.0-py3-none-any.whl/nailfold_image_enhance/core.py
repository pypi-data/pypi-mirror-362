import cv2
import numpy as np
from .exceptions import ProcessingError


def apply_clahe_enhance(image, config):
    """
    Apply CLAHE enhancement, denoising, and sharpening to a single frame

    Args:
        image (np.ndarray): Input image (BGR format, uint8)
        config (EnhanceConfig): Enhancement parameter configuration

    Returns:
        np.ndarray: Enhanced image (BGR format, uint8)
    """
    try:
        # Split BGR channels (OpenCV default format)
        b, g, r = cv2.split(image)

        # 1. Apply CLAHE enhancement
        clahe = cv2.createCLAHE(
            clipLimit=config.clip_limit,
            tileGridSize=config.tile_grid_size
        )
        b_clahe = clahe.apply(b)
        g_clahe = clahe.apply(g)
        r_clahe = clahe.apply(r)

        # 2. Non-local means denoising
        b_denoise = cv2.fastNlMeansDenoising(
            b_clahe,
            h=config.denoise_h,
            templateWindowSize=config.denoise_template_window,
            searchWindowSize=config.denoise_search_window
        )
        g_denoise = cv2.fastNlMeansDenoising(
            g_clahe,
            h=config.denoise_h,
            templateWindowSize=config.denoise_template_window,
            searchWindowSize=config.denoise_search_window
        )
        r_denoise = cv2.fastNlMeansDenoising(
            r_clahe,
            h=config.denoise_h,
            templateWindowSize=config.denoise_template_window,
            searchWindowSize=config.denoise_search_window
        )

        # 3. Gaussian blur sharpening (high-pass filter)
        b_blur = cv2.GaussianBlur(b_denoise, (0, 0), config.sharpen_sigma)
        g_blur = cv2.GaussianBlur(g_denoise, (0, 0), config.sharpen_sigma)
        r_blur = cv2.GaussianBlur(r_denoise, (0, 0), config.sharpen_sigma)

        b_sharpen = cv2.addWeighted(
            b_denoise, config.sharpen_alpha,
            b_blur, config.sharpen_beta, 0
        )
        g_sharpen = cv2.addWeighted(
            g_denoise, config.sharpen_alpha,
            g_blur, config.sharpen_beta, 0
        )
        r_sharpen = cv2.addWeighted(
            r_denoise, config.sharpen_alpha,
            r_blur, config.sharpen_beta, 0
        )

        # Merge channels and return
        return cv2.merge([b_sharpen, g_sharpen, r_sharpen])

    except Exception as e:
        raise ProcessingError(f"Image enhancement algorithm failed: {str(e)}")