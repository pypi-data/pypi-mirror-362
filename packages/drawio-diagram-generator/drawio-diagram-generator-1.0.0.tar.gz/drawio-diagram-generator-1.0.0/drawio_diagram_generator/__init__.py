"""
Draw.io Diagram Generator

A Python library for generating Draw.io diagrams programmatically.
"""

from .core import (
    DiagramComponent,
    Box,
    IconBox,
    Arrow,
    Line,
    Row,
    Column,
    Group,
    Diagram,
    save_diagram_to_file,
    build_style_string
)

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "DiagramComponent",
    "Box", 
    "IconBox",
    "Arrow",
    "Line",
    "Row",
    "Column", 
    "Group",
    "Diagram",
    "save_diagram_to_file",
    "build_style_string"
] 