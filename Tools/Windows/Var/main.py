import os

import yaml

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)


def initVar(window):
    # https://new.qq.com/rain/a/20211014a002rs00
    # 将宠物正常待机状态的动图放入pet1中
    window.pet1 = []
    for i in os.listdir("./pikaqiu"):
        window.pet1.append("pikaqiu/" + i)
    # 将宠物正常待机状态的对话放入pet2中

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