import yaml
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie, QTextList, QTextLine
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QTextEdit, QPushButton, QLineEdit, QHBoxLayout, QWidget, QFrame

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)

def initUI(window):
    # 设置窗口属性:窗口无标题栏且固定在最前面
    # FrameWindowHint:无边框窗口
    # WindowStaysOnTopHint: 窗口总显示在最上面
    # SubWindow: 新窗口部件是一个子窗口，而无论窗口部件是否有父窗口部件
    # https://blog.csdn.net/kaida1234/article/details/79863146

    # 添加背景

    window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
    # window.setAutoFillBackground(True) # True表示的是自动填充背景,False为透明背景
    window.setAttribute(Qt.WA_TranslucentBackground, True) # 窗口透明，窗体空间不透明

    window.repaint() # 重绘组件、刷新

    initLayout(window)

    window.show() # 显示窗口



def initLayout(window):
    # 配置layout
    window.ToDoTitle = QLabel("ToDoList(右键打开控制板)")
    window.ToDoList = QTextEdit()
    window.ToDoList.setPlainText(window.TodoObj.get_plaintext())
    window.ControlTitle = QLabel("控制板")
    window.ContorlButton = QPushButton("打开/折叠")
    window.TextInput = QLineEdit()

    window.btn_add = QPushButton("添加") # 根据prompt，在todolist末尾添加工作项
    window.btn_adjust = QPushButton("调整") # 根据prompt，调整工作项
    window.btn_format = QPushButton("对齐格式") # 对齐工作项的文本格式
    window.btn_simple = QPushButton("完成一条") # 移除最上面一个工作项
    window.btn_report = QPushButton("生成日报") # 将当前已完成事项生成日报
    window.btn_reportcopy = QPushButton("复制日报") # 将当前列表输出到剪贴板中


    window.randomPosition() # 调用自定义的randomPosition，会使得宠物出现位置随机

    # 创建一个QWidget容器来放置hbox中的内容
    window.controlBoxWidget = QWidget()

    # 布局设置
    vbox = QVBoxLayout()
    vbox.addWidget(window.ToDoTitle)
    vbox.addWidget(window.ToDoList)
    vbox.addWidget(window.controlBoxWidget)

    ctrl_vbox = QVBoxLayout(window.controlBoxWidget)
    ctrl_vbox.addWidget(QLabel("控制板"))
    ctrl_vbox.addWidget(QLabel(" ▽ Prompt"))
    ctrl_vbox.addWidget(window.TextInput)
    ctrl_vbox.addWidget(QLabel(" ▽ Buttons"))

    ctrl_hbox = QHBoxLayout()
    ctrl_hbox.addWidget(window.btn_add)
    ctrl_hbox.addWidget(window.btn_adjust)
    ctrl_vbox.addLayout(ctrl_hbox)

    # line = QFrame()
    # line.setFrameShape(QFrame.HLine)  # 设置成水平线
    # line.setFrameShadow(QFrame.Sunken)  # 可选，设置边框阴影
    # ctrl_vbox.addWidget(line)

    ctrl_hbox = QHBoxLayout()
    ctrl_hbox.addWidget(window.btn_format)
    ctrl_hbox.addWidget(window.btn_simple)
    ctrl_vbox.addLayout(ctrl_hbox)

    ctrl_hbox = QHBoxLayout()
    ctrl_hbox.addWidget(window.btn_report)
    ctrl_hbox.addWidget(window.btn_reportcopy)
    ctrl_vbox.addLayout(ctrl_hbox)

    window.controlBoxWidget.setVisible(False) # 隐藏控制板

    # 加载布局：前面设置好的垂直布局
    window.setLayout(vbox)


