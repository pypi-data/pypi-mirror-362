"""
dataframe2image - Convert pandas DataFrame to beautiful table images
"""

from .core import df_to_image, df_to_html, get_chinese_fonts
from .styles import TableStyle

__version__ = "0.1.0"
__all__ = ["df_to_image", "df_to_html", "get_chinese_fonts", "TableStyle"]
