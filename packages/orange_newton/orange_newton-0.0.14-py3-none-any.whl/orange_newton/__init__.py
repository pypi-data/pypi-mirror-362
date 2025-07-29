from importlib.metadata import version

from .main import hello

__version__ = version(__package__)
__copyright__ = "Copyright (C) 2020 Hiroshi Fujiwara"
__license__ = "MIT"
__author__ = "Hiroshi Fujiwara"
__author_email__ = "hiroshi.829f@gmail.com"
__url__ = "http://github.com/account/repository"
__all__ = ["hello"]
