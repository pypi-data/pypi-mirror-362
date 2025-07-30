from importlib.metadata import PackageNotFoundError, version

from .core import TDMRSDM

try:
    __version__ = version("tdmrsdm")
except PackageNotFoundError:
    # package is not installed
    __version__ = "unknown"