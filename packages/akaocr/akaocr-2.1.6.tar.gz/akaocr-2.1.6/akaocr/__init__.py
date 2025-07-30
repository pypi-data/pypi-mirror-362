# Writer: LauNT - 07/2025 - akaOCR Team

from .detect import BoxEngine
from .recog import TextEngine
from .rotate import ClsEngine

__version__ = 'akaocr-v2.1.6'
__all__ = ['BoxEngine', 'TextEngine', 'ClsEngine']
