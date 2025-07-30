"""
DevMe - Developer Dashboard Tool

A lightweight sidecar dashboard that provides developers with instant visibility 
into their project's health, configuration status, and development environment.
"""

__version__ = "0.2.1"
__author__ = "DevMe Contributors"
__email__ = "devme@citizentools.ai"
__description__ = "Developer dashboard for project health and configuration status"

from .core import DevMe
from .cli import main

__all__ = ["DevMe", "main"]