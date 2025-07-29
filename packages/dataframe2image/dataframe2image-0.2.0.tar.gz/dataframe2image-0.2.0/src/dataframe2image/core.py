"""
Core functionality for converting DataFrames to images
"""

import asyncio
import re
import tempfile
from pathlib import Path
from typing import Optional, Union, Dict

import pandas as pd
from playwright.async_api import async_playwright

from .styles import TableStyle, THEMES
from .template import render_dataframe_html


def get_chinese_fonts() -> Dict[str, str]:
    """Get available Chinese fonts from the font directory."""
    font_dir = Path(__file__).parent / "font"
    fonts = {}
    
    if font_dir.exists():
        for font_file in font_dir.glob("*.TTF"):
            # 使用字体文件名作为字体族名称
            font_name = font_file.stem.replace("_", " ")
            fonts[font_name] = str(font_file.absolute())
    
    return fonts


def contains_chinese_characters(df: pd.DataFrame) -> bool:
    """
    Check if the DataFrame contains Chinese characters.
    
    Args:
        df: The pandas DataFrame to check
        
    Returns:
        bool: True if Chinese characters are found, False otherwise
    """
    # Chinese character unicode ranges
    chinese_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\u20000-\u2a6df\u2a700-\u2b73f\u2b740-\u2b81f\u2b820-\u2ceaf]')
    
    # Check column names
    for col in df.columns:
        if isinstance(col, str) and chinese_pattern.search(col):
            return True
    
    # Check index values
    for idx in df.index:
        if isinstance(idx, str) and chinese_pattern.search(idx):
            return True
    
    # Check cell values
    for col in df.columns:
        for value in df[col]:
            if isinstance(value, str) and chinese_pattern.search(value):
                return True
    
    return False


async def _capture_table_screenshot(
    html_content: str,
    output_path: Union[str, Path],
    width: Optional[int] = None,
    height: Optional[int] = None,
    format: str = "png"
) -> None:
    """Capture screenshot of HTML table using Playwright."""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Set a larger default viewport to ensure all content is visible
        if width:
            viewport_height = height or 1200  # 增大默认高度
            await page.set_viewport_size({"width": width, "height": viewport_height})
        else:
            # 如果没有指定宽度，设置一个较大的默认视窗
            await page.set_viewport_size({"width": 1200, "height": 1200})
        
        # Load HTML content
        await page.set_content(html_content)
        
        # Wait for content to load and ensure all elements are rendered
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(1000)  # 额外等待确保渲染完成
        
        # Find the table container element
        table_element = await page.query_selector('.table-container')
        
        if table_element:
            # Screenshot just the table
            screenshot_options = {"path": str(output_path)}
            if format in ["png", "jpeg"]:
                screenshot_options["type"] = format
            await table_element.screenshot(**screenshot_options)
        else:
            # Fallback: screenshot the entire page
            screenshot_options = {"path": str(output_path), "full_page": True}
            if format in ["png", "jpeg"]:
                screenshot_options["type"] = format
            await page.screenshot(**screenshot_options)
        
        await browser.close()


def df_to_image(
    df: pd.DataFrame,
    output_path: Union[str, Path],
    style: Optional[Union[str, TableStyle]] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    format: str = "png",
    show_index: bool = True
) -> None:
    """
    Convert a pandas DataFrame to a table image.
    
    Args:
        df: The pandas DataFrame to convert
        output_path: Path where the image will be saved
        style: Either a TableStyle object or theme name string
        width: Image width in pixels (optional)
        height: Image height in pixels (optional)
        format: Image format ('png', 'jpeg', 'webp')
        show_index: Whether to show the DataFrame index
    
    Raises:
        ValueError: If the DataFrame is empty or invalid format specified
        RuntimeError: If screenshot capture fails
    """
    
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    if format.lower() not in ["png", "jpeg", "webp"]:
        raise ValueError(f"Unsupported format: {format}")
    
    # Note: Playwright only supports png and jpeg for element screenshots
    # WebP format will be saved as PNG with webp extension for compatibility
    actual_format = format.lower() if format.lower() in ["png", "jpeg"] else "png"
    
    # Handle style parameter
    if isinstance(style, str):
        if style in THEMES:
            style = THEMES[style]
        else:
            raise ValueError(f"Unknown theme: {style}")
    elif style is None:
        style = TableStyle()
    
    # 自动检测中文字符并设置字体
    font_files = None
    if contains_chinese_characters(df):
        font_files = get_chinese_fonts()
        if font_files:
            # 使用方正兰亭圆字体作为主要字体
            chinese_font_names = list(font_files.keys())
            style.font_family = f"'{chinese_font_names[0]}', 'Microsoft YaHei', 'SimHei', sans-serif"
    
    # Render HTML
    try:
        html_content = render_dataframe_html(df, style, show_index, font_files)
    except Exception as e:
        raise RuntimeError(f"Failed to render HTML: {e}")
    
    # Convert to image
    try:
        asyncio.run(_capture_table_screenshot(
            html_content, output_path, width, height, actual_format
        ))
    except Exception as e:
        raise RuntimeError(f"Failed to capture screenshot: {e}")


def df_to_html(
    df: pd.DataFrame,
    style: Optional[Union[str, TableStyle]] = None,
    show_index: bool = True
) -> str:
    """
    Convert a pandas DataFrame to styled HTML.
    
    Args:
        df: The pandas DataFrame to convert
        style: Either a TableStyle object or theme name string
        show_index: Whether to show the DataFrame index
    
    Returns:
        HTML string of the styled table
    """
    
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    # Handle style parameter
    if isinstance(style, str):
        if style in THEMES:
            style = THEMES[style]
        else:
            raise ValueError(f"Unknown theme: {style}")
    elif style is None:
        style = TableStyle()
    
    # 自动检测中文字符并设置字体
    font_files = None
    if contains_chinese_characters(df):
        font_files = get_chinese_fonts()
        if font_files:
            # 使用方正兰亭圆字体作为主要字体
            chinese_font_names = list(font_files.keys())
            style.font_family = f"'{chinese_font_names[0]}', 'Microsoft YaHei', 'SimHei', sans-serif"
    
    return render_dataframe_html(df, style, show_index, font_files)


def save_temp_html(html_content: str) -> str:
    """Save HTML content to a temporary file and return the path."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        return f.name
