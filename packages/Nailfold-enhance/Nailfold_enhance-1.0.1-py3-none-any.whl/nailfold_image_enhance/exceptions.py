class MedicalEnhanceError(Exception):
    """Base exception for enhancement processing"""
    pass


class FileNotFoundError(MedicalEnhanceError):
    """Exception raised when input file is not found"""

    def __init__(self, path):
        super().__init__(f"Input file not found: {path}")


class FormatNotSupportedError(MedicalEnhanceError):
    """Exception raised when file format is not supported"""

    def __init__(self, fmt):
        super().__init__(f"Unsupported format: {fmt}")


class ProcessingError(MedicalEnhanceError):
    """Exception raised when processing fails"""

    def __init__(self, msg):
        super().__init__(f"Processing failed: {msg}")
