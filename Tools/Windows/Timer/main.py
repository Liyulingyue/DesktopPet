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
    window.talkTimer.timeout.connect(window.talk)
    window.talkTimer.start(5000)

    # 休息一下
    window.timer_rest = QTimer()
    window.timer_rest.timeout.connect(window.haveRest)
    # window.timer_rest.start(10000)
    # window.timer_rest_movie = QTimer()
    # window.timer_rest_movie.timeout.connect(window.haveRestMovie)
    # window.timer_rest_movie.start(10000)