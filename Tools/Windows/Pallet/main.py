import webbrowser

import yaml
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)

# 初始化托盘菜单，用于主窗口程序
def initPallet(window):
    # 导入准备在托盘化显示上使用的图标
    icons = config_dict['Icon']

    # 新建一个菜单项控件
    menu = QMenu(window)

    # 设置托盘菜单项
    actions = {
        "show": QAction('显示界面', window, triggered=lambda: window.setWindowOpacity(1)), # 菜单项显示，配置透明度
        "hide": QAction('隐藏到托盘', window, triggered=lambda: window.setWindowOpacity(0)), # 菜单项隐藏，配置透明度
        "ernie": QAction('打开文心一言', window, triggered=lambda: webbrowser.open("https://yiyan.baidu.com")),  # 打开网页
    }


    # 设置点击选项的图片
    # quit_action.setIcon(QIcon(icons))

    # 将菜单项添加到菜单中
    for key in actions:
        action = actions[key]
        menu.addAction(action)



    if config_dict['DesktopPet'] == 1:
        menu.addAction(QAction('与桌面宠物交互', window, triggered=window.desktop_page.show))

    # 添加退出菜单项
    menu.addAction(QAction('退出', window, triggered=window.quit))

    # 配置图标并展示
    menu_icon = QSystemTrayIcon(window)
    menu_icon.setIcon(QIcon(icons)) # 设置托盘图标
    menu_icon.setContextMenu(menu) # 设置托盘菜单

    # 配置托盘左键单击事件
    menu_icon.activated.connect(lambda click_type: actions["show"].trigger() if click_type == QSystemTrayIcon.Trigger else None)
    menu_icon.show() # 展示