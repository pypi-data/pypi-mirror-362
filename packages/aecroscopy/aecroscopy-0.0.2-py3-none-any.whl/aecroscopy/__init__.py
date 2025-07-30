"""
The aecroscopy package
"""

from .__version__ import version as __version__
from . import base, communication, acquisition, processing, utilities

from .base import *
from .communication import *
from .acquisition import *
from .processing import *
from .utilities import *

__all__ = ['__version__']
__all__ += communication.__all__
__all__ += acquisition.__all__
__all__ += base.__all__
__all__ += processing.__all__
__all__ += utilities.__all__
