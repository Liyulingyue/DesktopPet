import os

import yaml

from ..chatbot import ChatBox

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)


def initVar(window):
    # 配置对话信息
    window.dialog = []
    with open(config_dict["Dialog"], "r") as f: # 读取目录下dialog文件
        text = f.read()
        # 以\n 即换行符为分隔符，分割放进dialog中
        window.dialog = text.split("\n")

    '''
    宠物状态应当为：
    Normal: 正常待机
    Hang: 鼠标长按拖拽
    Rest: 休息
    '''
    window.petstate = "Normal" # 宠物状态

    '''
    宠物对话状态应当为：
    Normal: 正常对话
    Hang: 鼠标长按拖拽，停止对话
    '''
    window.talkstate = "Normal" # 宠物对话状态

    '''
    宠物休息状态应当为：
    Normal: 正常
    Rest: 休息
    '''
    window.reststate = "Normal" # 宠物休息状态

    window.is_follow_mouse = False # 是否跟随鼠标
    window.mouse_drag_pos = None # 拖拽事件的辅助变量
    window.chatbox = ChatBox() # 初始化聊天框