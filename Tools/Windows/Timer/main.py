import os

import yaml
from PyQt5.QtCore import QTimer

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)

def initTimer(window):
    # 画面切换
    window.timer = QTimer() # 定时器设置
    window.timer.timeout.connect(window.refreshMovie) # 绑定结束时动作
    window.timer.start(5000) # 动作时间切换设置

    # 每隔一段时间切换对话
    window.talkTimer = QTimer()
    window.talkTimer.timeout.connect(window.refreshTalk)
    window.talkTimer.start(5000)