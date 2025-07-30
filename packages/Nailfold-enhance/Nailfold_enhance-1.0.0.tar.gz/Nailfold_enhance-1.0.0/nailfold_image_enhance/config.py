class EnhanceConfig:
    """Configuration class for enhancement algorithm parameters (default values optimized for medical imaging)"""
    def __init__(self):
        # CLAHE parameters
        self.clip_limit = 2.0          # Contrast limit (default 2.0, range 1.0-10.0)
        self.tile_grid_size = (8, 8)   # Tile grid size (default 8x8, recommended 3-16)
        # Denoising parameters
        self.denoise_h = 12            # Non-local means denoising strength (default 12, range 5-30)
        self.denoise_template_window = 7  # Denoising template window (default 7, odd number)
        self.denoise_search_window = 21   # Denoising search window (default 21, odd number)
        # Sharpening parameters (Gaussian blur weights)
        self.sharpen_alpha = 1.5       # Original image weight (default 1.5)
        self.sharpen_beta = -0.5       # Blurred image weight (default -0.5)
        self.sharpen_sigma = 80        # Gaussian blur sigma (default 80)

    def update(self, **kwargs):
        """Dynamically update parameters (supports keyword arguments)"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unsupported parameter: {key}")