# -*- coding: utf-8 -*-
# __init__.py

__version__ = "1.3.0"

from .binning import reBin
from .git import checkRepo, isNBstripoutActivated, isNBstripoutInstalled, isRepo
from .readdata import readdata
from .readdata import readdata as readPDH
from .readdata import readPDHmeta, readSSF
from .utils import setLocaleUTF8
from .widgets import PathSelector, showBoolStatus

setLocaleUTF8()
