import os
import sys
import random
import time

import yaml
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .Method.petchatbox import initMethods
from .UI.petchatbox import initUI
from .Var.petchatbox import initVar

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)

class PetChatBox(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(PetChatBox, self).__init__(parent)

        # 若**kwargs不为空，则保存传入信息
        if kwargs != {}:
            for key in kwargs:
                setattr(self, key, kwargs[key])

        initVar(self)
        initUI(self)
        initMethods(self)

    def closeEvent(self, event):
        self.SerialObj.close_serial()

