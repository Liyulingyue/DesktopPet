import yaml
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel, QVBoxLayout

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)

def initUI(window):
    # 设置窗口属性:窗口无标题栏且固定在最前面
    # FrameWindowHint:无边框窗口
    # WindowStaysOnTopHint: 窗口总显示在最上面
    # SubWindow: 新窗口部件是一个子窗口，而无论窗口部件是否有父窗口部件
    # https://blog.csdn.net/kaida1234/article/details/79863146

    window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
    window.setAutoFillBackground(False) # True表示的是自动填充背景,False为透明背景
    window.setAttribute(Qt.WA_TranslucentBackground, True) # 窗口透明，窗体空间不透明

    window.repaint() # 重绘组件、刷新

    initLayout(window)

    window.show() # 显示窗口

def initLayout(window):
    # 配置layout

    window.talkLabel = QLabel(window) # 对话框定义
    window.talkLabel.setStyleSheet("font:15pt '楷体';border-width: 1px;color:blue;") # 对话框样式设计

    window.image = QLabel(window) # 定义显示图片部分
    window.movie = QMovie("pikaqiu/pikaqiu1.gif") # QMovie是一个可以存放动态视频的类，一般是配合QLabel使用的,可以用来存放GIF动态图
    window.movie.setScaledSize(QSize(200, 200)) # 设置标签大小
    window.image.setMovie(window.movie) # 将Qmovie在定义的image中显示
    window.movie.start()
    # window.resize(300, 300)


    window.show_time_rest = QLabel(window) # "休息一下"时间显示
    window.show_time_rest.setStyleSheet("font:15pt '楷体';border-width: 1px;color:blue;") # 对话框样式设计


    window.randomPosition() # 调用自定义的randomPosition，会使得宠物出现位置随机

    # 布局设置
    vbox = QVBoxLayout()
    vbox.addWidget(window.talkLabel)
    vbox.addWidget(window.image)
    vbox.addWidget(window.show_time_rest)

    # 加载布局：前面设置好的垂直布局
    window.setLayout(vbox)


