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

    def setMovie(self, movie_path):
        """
        设置动画并添加到标签中
        Args:
            movie_path (str): 动画文件路径(gif格式)
        """
        self.movie = QMovie(movie_path) # 读取图片路径
        self.movie.setScaledSize(QSize(200, 200)) # 宠物大小
        self.image.setMovie(self.movie) # 将动画添加到label中
        self.movie.start() # 开始播放动画


    # 随机动作切换
    def refreshMovie(self):
        # condition记录宠物状态，宠物状态为0时，代表正常待机
        if self.petstate == "Normal":
            movie_path = random.choice(self.pet1) # 随机选择装载在pet1里面的gif图进行展示，实现随机切换
            # condition不为0，转为切换特有的动作，实现宠物的点击反馈
            # 这里可以通过else-if语句往下拓展做更多的交互功能
        elif self.petstate == "Hang":
            # 读取特殊状态图片路径
            movie_path = "./click/click.gif"
            # 宠物状态设置为正常待机
            self.petstate = "Normal"
            self.talkstate = "Normal"
        elif self.petstate == "Rest":
            movie_path = "./click/20220614223056.gif" # 把表情设定为固定的动作
            # 宠物状态设置为正常待机
            # self.petstate = "Normal"

        self.setMovie(movie_path)
            

    # 宠物对话框行为处理
    def talk(self):
        if self.talkstate == "Normal":
            # talk_condition为0则选取加载在dialog中的语句
            self.talkLabel.setText(random.choice(self.dialog))
            # 设置样式
            self.talkLabel.setStyleSheet(
                "font: bold;"
                "font:15pt '楷体';"
                "color:white;"
                "background-color: white"
                "url(:/)"
            )
            # 根据内容自适应大小
            self.talkLabel.adjustSize()
        else:
            # talk_condition为1显示为别点我，这里同样可以通过if-else-if来拓展对应的行为
            self.talkLabel.setText("咬你哦！")
            self.talkLabel.setStyleSheet(
                "font: bold;"
                "font:15pt '楷体';"
                "color:white;"
                "background-color: white"
                "url(:/)"
            )
            self.talkLabel.adjustSize()
            # self.talkLabel.
            # 设置为正常状态
            self.talkstate = "Normal"

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
        self.petstate = "Hang"  # 更改宠物状态为点击
        self.talkstate = "Hang"  # 更改宠物对话状态

        self.talk() # 即可调用对话状态改变
        self.refreshMovie() # 即刻加载宠物点击动画

        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True

        # globalPos() 事件触发点相对于桌面的位置
        # pos() 程序相对于桌面左上角的位置，实际是窗口的左上角坐标
        self.mouse_drag_pos = event.globalPos() - self.pos()
        event.accept()
        # 拖动时鼠标图形的设置
        self.setCursor(QCursor(Qt.OpenHandCursor))

        # 取消休息状态
        self.show_time_rest.setText("")

    # 鼠标移动时调用，实现宠物随鼠标移动
    def mouseMoveEvent(self, event):
        # 如果鼠标左键按下，且处于绑定状态
        if Qt.LeftButton and self.is_follow_mouse:
            # 宠物随鼠标进行移动
            self.move(event.globalPos() - self.mouse_drag_pos)
        event.accept()

    # 鼠标释放调用，取消绑定
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        # 鼠标图形设置为箭头
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 鼠标移进时调用
    def enterEvent(self, event):
        # 设置鼠标形状 Qt.ClosedHandCursor   非指向手
        self.setCursor(Qt.ClosedHandCursor)

    # 宠物右键点击交互
    def contextMenuEvent(self, event):
        # 定义菜单
        menu = QMenu(self)
        # 定义菜单项
        hide = menu.addAction("隐藏")
        question_answer = menu.addAction("文心一言")
        if self.reststate == "Normal":
            rest_anhour = menu.addAction("打开休息提醒")
        elif self.reststate == "Rest":
            rest_anhour = menu.addAction("关闭休息提醒")
        menu.addSeparator()
        quitAction = menu.addAction("退出")

        # 使用exec_()方法显示菜单。从鼠标右键事件对象中获得当前坐标。mapToGlobal()方法把当前组件的相对坐标转换为窗口（window）的绝对坐标。
        action = menu.exec_(self.mapToGlobal(event.pos()))
        # 点击事件为退出
        if action == quitAction:
            qApp.quit()
        # 点击事件为隐藏
        if action == hide:
            # 通过设置透明度方式隐藏宠物
            self.setWindowOpacity(0)
        # 点击事件为故事大会
        if action == question_answer:
            self.chatbox = ChatBox()
            self.chatbox.show()

        # 打开休息提醒
        if action == rest_anhour:
            if self.reststate == "Normal":
                self.timer_rest.start(3600000)
                self.reststate = "Rest"
            elif self.reststate == "Rest":
                self.timer_rest.stop()
                self.reststate = "Normal"

    # 休息时间
    def haveRest(self):
        self.show_time_rest.setText("休息一下")
        self.show_time_rest.setStyleSheet(
                "font: bold;"
                "font:25pt '楷体';"
                "color:white;"
                "background-color: white"
                "url(:/)"
            )
        
        # 固定休息图标
        self.petstate = "Rest"
        self.refreshMovie()
        # screenGeometry（）函数提供有关可用屏幕几何的信息
        screen_geo = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width())
        height = (screen_geo.height() - pet_geo.height())
        self.move(width / 2, height / 2)
    

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
