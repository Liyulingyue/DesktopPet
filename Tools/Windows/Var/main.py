import os

import yaml

from ..chatbot import ChatBox

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)


def initVar(window):
    '''
    宠物状态应当为：
    Normal: 正常待机
    Hang: 鼠标长按拖拽
    Rest: 休息
    '''
    window.HideInputFlag = False

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

    if config_dict["LLM"] == "ernie":
        from ...LLM.ernie import ErnieClass
        window.llm = ErnieClass(config_dict.get("ErnieToken", ""))
    elif config_dict["LLM"] == "glm3":
        from ...LLM.glm3 import GLM3Class
        window.llm = GLM3Class(config_dict.get("GLM3Directory", ""))
    elif config_dict["LLM"] == "GRADIO":
        from ...LLM.gr_server import GradioClass
        window.llm = GradioClass(config_dict.get("GradioURL", ""))
    else:
        window.llm = None

    window.TodoUpdateFlag = False
    window.TodoUpdateContent = ""