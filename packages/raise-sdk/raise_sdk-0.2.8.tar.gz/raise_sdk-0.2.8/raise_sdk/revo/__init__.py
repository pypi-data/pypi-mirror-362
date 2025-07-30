"""RAISE SDK Remote Execution Validation Operations"""

import os
import sys
path = os.path.abspath(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app')
if path not in sys.path:
    sys.path.append(path)

from . import app
from .main import processing_script_execution as start

__all__ = [
    "app",
    "start",
]