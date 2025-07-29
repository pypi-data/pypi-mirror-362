"""
Tailwind CSS styling module for ReactPy.
"""

__version__ = '1.0.1-Alpha'
__name__ = 'tailwindcss'

from .Configuration import configure as configure_tailwind, default_style as default_tailwind

__all__ = ['configure_tailwind', 'default_tailwind']