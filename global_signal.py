import sys
import PySide6.QtWidgets as pq
from PySide6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QHideEvent
from PySide6.QtCore import Signal, QObject
import random


# documentation to functools https://docs.python.org/3/library/functools.html

#global
class SignalSharingObject(QObject):
    my_Signal = Signal()
    
signal_sharing_obj = SignalSharingObject()

