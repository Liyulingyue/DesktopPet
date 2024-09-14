import yaml
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import sys
import socket
from threading import Thread

from ..LLM.ernie import ErnieClass

# from transformers import BertTokenizer, GPT2LMHeadModel, TextGenerationPipeline
# tokenizer = BertTokenizer.from_pretrained("./text_generator/")
# model = GPT2LMHeadModel.from_pretrained("./text_generator/")
# text_generator = TextGenerationPipeline(model, tokenizer)

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)
if "ErnieToken" not in config_dict:
    config_dict['ErnieToken'] = "1111111111" #赋无效值避免报错

class ChatBox(QWidget):
    # 初始化界面
    def __init__(self, parent=None, **kwargs):
        # QWidget.__init__(self)
        super(ChatBox, self).__init__(parent)

        self.init()

        self.add_ui()

        self.llm = ErnieClass(access_token=config_dict['ErnieToken'])
 
        # 启动线程
        self.work_thread()

        # # 展示
        # self.show()

    def init(self):

        # 设置窗口的大小和位置
        self.setGeometry(600, 300, 600, 337)
        # 设置标题
        self.setWindowTitle("文心一言")

        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)

        # setAutoFillBackground(True)表示的是自动填充背景,False为透明背景
        self.setAutoFillBackground(False)
        # 窗口透明，窗体空间不透明
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        # 重绘组件、刷新
        self.repaint()

 
    # 设置界面当中的组件
    def add_ui(self):
        # 多行文本显示，显示所有的聊天信息
        self.content = QTextBrowser(self)
        self.content.setGeometry(30, 30, 550, 150)
 
        # 单行文本，消息发送框
        self.message = QLineEdit(self)
        self.message.setGeometry(30, 220, 550, 30)
        self.message.setPlaceholderText("请输入发送内容")
 
        # 发送按钮
        self.button = QPushButton("发送", self)
        self.button.setFont(QFont("微软雅黑", 10, QFont.Bold))
        self.button.setGeometry(520, 270, 60, 30)

        # 关闭按钮
        self.btn_close = QPushButton("关闭", self)
        self.btn_close.setFont(QFont("微软雅黑", 10, QFont.Bold))
        self.btn_close.setGeometry(420, 270, 60, 30)

        self.btn_close.clicked.connect(self.closeEvent)
 
 
    # 发送消息 + 接收消息
    def send_msg(self):
        selfname = config_dict['UserName']
        agentname = config_dict['AgentName']
        msg = self.message.text()

        self.content.append(f"{selfname}: {msg}")

        self.message.clear()

        msg = [
            {'role': "user", 'content': f"我的身份是{selfname}，请你扮演{agentname},与我对话。如果你理解我的意图请回复 好的 。"},
            {'role': "assistant", 'content': "好的"},
            {'role': "user", 'content': msg}
        ]

        # text_output = self.llm.get_llm_answer(msg)
        text_output = self.llm.get_llm_answer_with_msg(msg)


        self.content.append(f"{agentname}: {text_output}")

    # 接收消息
    def recv_msg(self):
        while True:
            data = self.message.text().encode()
            print(type(data))
            if data != "" or data is not None:
                # print(data + "12312")
                data = str(data) + "\n"
                self.content.append(data)
            else:
                exit()
 
    # 点击按钮发送消息
    def btn_send(self):
        self.button.clicked.connect(self.send_msg)
 
    # 线程处理
    def work_thread(self):
        Thread(target=self.btn_send).start()
        # Thread(target=self.recv_msg).start()

    # 推出销毁对话窗口
    def closeEvent(self, event):
        self.destroy()


if __name__ == '__main__':
    # 创建了一个QApplication对象，对象名为app，带两个参数argc,argv
    # 所有的PyQt5应用必须创建一个应用（Application）对象。sys.argv参数是一个来自命令行的参数列表。
    app = QApplication(sys.argv)
    # 窗口组件初始化
    chatbox = ChatBox()
    ChatBox.show()
    # 1. 进入时间循环；
    # 2. wait，直到响应app可能的输入；
    # 3. QT接收和处理用户及系统交代的事件（消息），并传递到各个窗口；
    # 4. 程序遇到exit()退出时，机会返回exec()的值。
    sys.exit(app.exec_())
