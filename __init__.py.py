"""
Layered-Earth: Geospatial Special Support System
A comprehensive geospatial analysis library with interactive mapping capabilities.
"""

__version__ = "1.0.0"
__author__ = "neovenator99"

from layered_earth.ui.main_app import launch_app

def launch():
    """Launch the Layered-Earth application"""
    return launch_app()

def quick_start():
    """Quick start with sample data"""
    app = launch_app()
    return app

__all__ = ['launch', 'quick_start']