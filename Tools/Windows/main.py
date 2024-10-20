import os
import sys
import random
import time

import yaml
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .Method.main import initLLMMethods, initRightClickMenu
from .Timer.main import initTimer # 初始化定时器
from .Var.main import initVar # 初始化变量
from .UI.main import initUI # 初始化界面
from .Pallet.main import initPallet # 初始化托盘参数

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
        initTimer(self) # 初始化定时器
        initUI(self) # 初始化界面
        initPallet(self) # 托盘化初始

        # 当前实现中，该部分代码用了很多之前定义的变量，必须放在后面
        initLLMMethods(self) # 初始化方法和button的关联
        initRightClickMenu(self) # 初始化菜单

    def updateTodo(self):
        if self.TodoUpdateFlag:
            self.ToDoList.setPlainText(self.TodoUpdateContent)
            self.TodoUpdateFlag = False
            self.ToDoTitle.setText("ToDoList(右键打开控制板)")
            self.ButtonLock = False

    # 退出操作，关闭程序
    def quit(self):
        self.saveToDoList()
        self.close()
        sys.exit()

    def saveToDoList(self):
        # 获取待办事项列表
        todo_list = self.ToDoList.toPlainText()
        self.TodoObj.update_todolist(todo_list)
        self.TodoObj.save()


    def paintEvent(self, event):
        # 绘制半透明白色背景
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        color = QtGui.QColor(173, 216, 230, 160)  # 白色: 255, 255, 255，透明度：50% 透明度 (255 * 0.5 = 128)
        painter.fillRect(self.rect(), color)
        painter.end()

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
            self.is_follow_mouse = True # 设置为绑定状态
            # 获取窗口的位置
            #   globalPos() 事件触发点相对于桌面的位置
            #   pos() 程序相对于窗口父控件（可能是屏幕）的左上角坐标
            self.mouse_drag_pos = event.globalPos() - self.pos()

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
            self.is_follow_mouse = False

            self.setCursor(QCursor(Qt.ArrowCursor)) # 鼠标图形设置为箭头

    # 宠物右键点击交互
    def contextMenuEvent(self, event):
        # 弹出菜单，menu.exec_()方法用于显示一个弹出菜单（通常是一个QMenu实例），并等待用户选择一个动作
        # 该方法会阻塞当前的事件循环，直到用户选择了菜单中的一个项或关闭了菜单
        action = self.menu.exec_(self.mapToGlobal(event.pos()))
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
