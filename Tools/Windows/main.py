import os
import sys
import random
import time

import yaml
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .Timer.main import initTimer # 初始化定时器
from .Var.main import initVar # 初始化变量
from .UI.main import initUI # 初始化界面
from .Pallet.main import initPallet # 初始化托盘参数
from .chatbot import ChatBox

# from transformers.dependency_versions_check import pkgs_to_check_at_runtime
# print(pkgs_to_check_at_runtime)

# config_dict = yaml.safe_load(
#     open(
#         os.path.join(os.getcwd(), 'Source/config.yaml')
#     )
# )
config_dict = yaml.safe_load(
    open('Source/config.yaml')
)

class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)

        initVar(self) # 初始化变量
        initUI(self) # 初始化界面
        initPallet(self) # 托盘化初始
        initTimer(self) # 初始化定时器

        self.refreshMovie() # 初始化宠物动作
        self.refreshTalk() # 初始化对话


    def setMovie(self, movie_path):
        """
        设置动画并添加到标签中
        Args:
            movie_path (str): 动画文件路径(gif格式)
        """
        self.movie = QMovie(movie_path) # 读取图片路径
        self.movie.setScaledSize(QSize(config_dict["Image_size"][0], config_dict["Image_size"][1])) # 宠物大小
        self.image.setMovie(self.movie) # 将动画添加到label中
        self.movie.start() # 开始播放动画


    # 随机动作切换
    def refreshMovie(self):
        """
        刷新宠物动画。
        """
        if self.petstate == "Normal":
            movie_path = random.choice(config_dict["Images"]["Normal"]) # 随机选择通用动作
        elif self.petstate == "Hang":
            movie_path = config_dict["Images"]["Hang"]
        else:
            movie_path = random.choice(config_dict["Images"]["Normal"])

        self.setMovie(movie_path)
            

    def setTalk(self, text):
        """
        设置对话内容。
        Args:
            text (str): 文本内容
        """
        self.talkLabel.setText(text)
        self.talkLabel.setStyleSheet(
            "font: bold;"
            "font:15pt '楷体';"
            "color:white;"
            "background-color: white"
            "url(:/)"
        )
        self.talkLabel.adjustSize()

    # 宠物对话框行为处理
    def refreshTalk(self):
        if self.talkstate == "Normal":
            text = random.choice(self.dialog) # 随机选择对话内容
        else: # Hang
            text = "咬你哦！"
            self.talkstate = "Normal" # 设置为正常状态

        self.setTalk(text) # 设置对话内容

    # 退出操作，关闭程序
    def quit(self):
        self.close()
        sys.exit()

    # 宠物随机位置
    def randomPosition(self):
        # screenGeometry（）函数提供有关可用屏幕几何的信息
        screen_geo = QDesktopWidget().screenGeometry()

        pet_geo = self.geometry() # 获取窗口坐标系
        width = int((screen_geo.width() - pet_geo.width()) * random.random())
        height = int((screen_geo.height() - pet_geo.height()) * random.random())
        self.move(width, height)

    # 鼠标左键按下时, 宠物将和鼠标位置绑定
    def mousePressEvent(self, event):
        # 判断是否为鼠标左键
        if event.button() == Qt.LeftButton:
            # 宠物点击状态为点击
            self.petstate = "Hang"  # 更改宠物状态为点击
            self.talkstate = "Hang"  # 更改宠物对话状态
            self.is_follow_mouse = True # 设置为绑定状态
            # 获取窗口的位置
            #   globalPos() 事件触发点相对于桌面的位置
            #   pos() 程序相对于窗口父控件（可能是屏幕）的左上角坐标
            self.mouse_drag_pos = event.globalPos() - self.pos()


            self.refreshTalk() # 刷新对话
            self.refreshMovie() # 刷新动画
            self.setCursor(QCursor(Qt.OpenHandCursor)) # 拖动时鼠标图形的设置

            event.accept()

    # 鼠标移动时调用，实现宠物随鼠标移动
    def mouseMoveEvent(self, event):
        # 如果鼠标左键按下，且处于绑定状态
        if (event.buttons() & Qt.LeftButton) and self.is_follow_mouse:
            # 宠物随鼠标进行移动
            self.move(event.globalPos() - self.mouse_drag_pos)
        event.accept()

    # 鼠标释放调用，取消绑定
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.petstate = "Normal"  # 更改宠物状态为点击
            self.talkstate = "Normal"  # 更改宠物对话状态
            self.is_follow_mouse = False

            self.setCursor(QCursor(Qt.ArrowCursor)) # 鼠标图形设置为箭头
            self.refreshMovie()  # 刷新动画
            self.refreshTalk() # 刷新对话

    # 鼠标移进时调用
    def enterEvent(self, event):
        # 设置鼠标形状 Qt.ClosedHandCursor   非指向手
        self.setCursor(Qt.ClosedHandCursor)

    # 宠物右键点击交互
    def contextMenuEvent(self, event):
        # 定义菜单
        menu = QMenu(self)

        # 定义菜单项
        actions = {
            "hide": QAction('隐藏', self, triggered=lambda: self.setWindowOpacity(0)),
            "ernie": QAction('文心一言', self, triggered=lambda: self.chatbox.show()),
        }
        for key, value in actions.items():
            menu.addAction(value)

        # 添加分割线
        menu.addSeparator()

        # 添加退出菜单
        ActionQuit = QAction('退出', self, triggered=qApp.quit)
        menu.addAction(ActionQuit)

        # 弹出菜单
        # menu.exec_()方法用于显示一个弹出菜单（通常是一个QMenu实例），并等待用户选择一个动作
        # 该方法会阻塞当前的事件循环，直到用户选择了菜单中的一个项或关闭了菜单
        action = menu.exec_(self.mapToGlobal(event.pos()))
        # if action == ActionQuit:
        #     print("退出")

    

if __name__ == '__main__':
    # 创建了一个QApplication对象，对象名为app，带两个参数argc,argv
    # 所有的PyQt5应用必须创建一个应用（Application）对象。sys.argv参数是一个来自命令行的参数列表。
    app = QApplication(sys.argv)
    # 窗口组件初始化
    pet = DesktopPet()
    # 1. 进入时间循环；
    # 2. wait，直到响应app可能的输入；
    # 3. QT接收和处理用户及系统交代的事件（消息），并传递到各个窗口；
    # 4. 程序遇到exit()退出时，机会返回exec()的值。
    sys.exit(app.exec_())
