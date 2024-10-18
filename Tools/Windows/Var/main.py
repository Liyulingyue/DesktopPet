import os

import yaml

from ...Classes.TodoClass import TodoClass

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)


def initVar(window):
    window.is_follow_mouse = False # 是否跟随鼠标
    window.mouse_drag_pos = None # 拖拽事件的辅助变量

    # 若window存在属性llm，则直接使用window.llm作为LLM，否则根据配置文件中的LLM类型创建相应的LLM对象
    if hasattr(window, 'llm'):
        pass
    else:
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
    window.ButtonLock = False
    window.TodoObj = TodoClass()