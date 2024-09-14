import os

import yaml
from PyQt5.QtCore import QTimer

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)

def initTimer(window):
    # 画面切换
    window.timer = QTimer() # 定时器设置
    window.timer.timeout.connect(window.updateTodo) # 绑定结束时动作
    window.timer.start(config_dict["TodoUIUpdateTime"]) # 动作时间切换设置, 1000ms = 1s