"""
Style configuration for table rendering
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TableStyle:
    """Configuration for table styling."""
    
    theme: str = "light"
    font_family: str = "Arial, sans-serif"
    font_size: int = 12
    border_color: str = "#ddd"
    header_bg_color: str = "#f8f9fa"
    header_text_color: str = "#212529"
    row_bg_colors: Optional[List[str]] = None
    row_text_color: str = "#212529"
    border_width: int = 1
    cell_padding: str = "8px 12px"
    table_border_radius: str = "6px"
    box_shadow: str = "0 2px 8px rgba(0,0,0,0.1)"
    
    def __post_init__(self) -> None:
        """Set default row background colors if not provided."""
        if self.row_bg_colors is None:
            if self.theme == "dark":
                self.row_bg_colors = ["#2d3748", "#4a5568"]
                self.header_bg_color = "#1a202c"
                self.header_text_color = "#ffffff"
                self.row_text_color = "#ffffff"
                self.border_color = "#4a5568"
            elif self.theme == "minimal":
                self.row_bg_colors = ["#ffffff", "#ffffff"]
                self.border_color = "#e2e8f0"
                self.box_shadow = "none"
            else:  # light theme
                self.row_bg_colors = ["#ffffff", "#f8f9fa"]


# Predefined themes
THEMES = {
    "light": TableStyle(),
    "dark": TableStyle(theme="dark"),
    "minimal": TableStyle(theme="minimal"),
    "blue": TableStyle(
        header_bg_color="#007bff",
        header_text_color="#ffffff",
        row_bg_colors=["#ffffff", "#f8f9ff"],
        border_color="#007bff"
    ),
    "green": TableStyle(
        header_bg_color="#28a745",
        header_text_color="#ffffff",
        row_bg_colors=["#ffffff", "#f8fff8"],
        border_color="#28a745"
    ),
}
