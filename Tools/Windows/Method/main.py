import threading
import webbrowser

import pyperclip
from PyQt5.QtWidgets import QMessageBox, QMenu, QAction


def lockButton(window):
    # 锁定按钮，让其他点击事件无效
    if not window.ButtonLock:
        window.ButtonLock = True
        window.ToDoTitle.setText("正在处理...")
        return True
    else:
        return False

def addMethod(window, type="LLM"):
    if not lockButton(window): # 未成功，则返回
        return

    todotext = window.ToDoList.toPlainText() # 获取界面上的任务列表文本
    user_input = window.TextInput.text() # 获取用户输入的文本

    # 如果用户输入的文本不为空，则执行以下操作
    if not user_input.strip() == '':
        if type == "LLM":
            prompt = f"""
    请根据用户需求进行规划，并输出结果。
    用户的需求是：{user_input}
    请以json格式输出。输出内容是一个list[字典]，字典内容如下：
    [{'{'}
        Task: str，具体的任务内容
    {'}'}]
    如果任务需要拆分，则进行拆分，输出list中包含各个步骤。如果任务无需拆分，则输出仅含一个成员的list。
    """
            llm_result = window.llm.get_llm_json_answer(prompt)
            task_text = ""
            if isinstance(llm_result, list):
                for item in llm_result:
                    if isinstance(item, dict):
                        # task_text += f"{item.get('Time', -1)}h {item.get('Task')} Rank:{item.get('Priority')}\n"
                        task_text += f"{item.get('Task')}\n"
            # print(llm_result)
        else:
            task_text = user_input
    else:
        task_text = ""

    # 更新任务列表文本
    todotext = window.ToDoList.toPlainText()  # 获取界面上的任务列表文本

    if not todotext.endswith('\n') and todotext.strip() != '':
        todotext += '\n'
    todotext += task_text

    # 避免卡死，必须在主线程更新UI
    window.TodoUpdateContent = todotext
    window.TodoUpdateFlag = True

def adjustMethod(window):
    if not lockButton(window): # 未成功，则返回
        return

    todotext = window.ToDoList.toPlainText() # 获取界面上的任务列表文本
    user_input = window.TextInput.text() # 获取用户输入的文本

    # 如果用户输入的文本不为空，则执行以下操作
    if not user_input.strip() == '':
        # task_text = user_input
        prompt = f"""
请根据用户需求，对需求列表进行调整。
用户的需求是：{user_input}，当前的任务列表是：{todotext}。
请以json格式输出（特别的，请不要在json中增加注释等辅助性的说明文本）。输出内容是一个list[字典]，字典内容如下：
[{'{'}
    Task: str，具体的任务内容，
{'}'}]
输出list中包含各个事项。如果仅存在一个事项，则输出仅含一个成员的list。
        """
        llm_result = window.llm.get_llm_json_answer(prompt)
        task_text = ""
        if isinstance(llm_result, list):
            for item in llm_result:
                if isinstance(item, dict):
                    # task_text += f"{item.get('Time', -1)}h {item.get('Task')} Rank:{item.get('Priority')}\n"
                    task_text += f"{item.get('Task')}\n"
    else:
        task_text = todotext

    # 更新任务列表文本
    todotext = task_text

    # 避免卡死，必须在主线程更新UI
    window.TodoUpdateContent = todotext
    window.TodoUpdateFlag = True


def formatMethod(window):
    if not lockButton(window): # 未成功，则返回
        return

    todotext = window.ToDoList.toPlainText() # 获取界面上的任务列表文本
    user_input = window.TextInput.text() # 获取用户输入的文本

    prompt = (f"""
请对任务列表进行整理，并按照约定格式输出，如果任务列表中没有包含必要的信息，请自行推断并补充。
当前的任务列表是：{todotext}。
请以json格式输出。输出内容是一个list[字典]，字典内容如下：
[{'{'}
    Task: str，具体的任务内容，
{'}'}]
输出list中包含各个事项。如果仅存在一个事项，则输出仅含一个成员的list。
    """)
    llm_result = window.llm.get_llm_json_answer(prompt)

    task_text = ""
    if isinstance(llm_result, list):
        for item in llm_result:
            if isinstance(item, dict):
                # task_text += f"{item.get('Time', -1)}h {item.get('Task')} Rank:{item.get('Priority')}\n"
                task_text += f"{item.get('Task')}\n"
    # 更新任务列表文本
    todotext = task_text

    # 避免卡死，必须在主线程更新UI
    window.TodoUpdateContent = todotext
    window.TodoUpdateFlag = True


def archiveMethod(window):
    if not lockButton(window): # 未成功，则返回
        return

    todotext = window.ToDoList.toPlainText() # 获取界面上的任务列表文本
    window.TodoObj.update_todolist(todotext) # 更新任务列表
    window.TodoObj.archive()
    todotext = window.TodoObj.get_plaintext()

    # 避免卡死，必须在主线程更新UI
    window.TodoUpdateContent = todotext
    window.TodoUpdateFlag = True

def reportMethod(window, report_type="LLM"):
    # print("reportMethod")
    if not lockButton(window): # 未成功，则返回
        return

    todotext = window.ToDoList.toPlainText() # 获取界面上的任务列表文本
    window.TodoObj.generate_report(window.llm, report_type)

    # 避免卡死，必须在主线程更新UI
    window.TodoUpdateContent = todotext
    window.TodoUpdateFlag = True

def copyreportMethod(window):
    # print("copyreportMethod")
    if not lockButton(window): # 未成功，则返回
        return

    todotext = window.ToDoList.toPlainText() # 获取界面上的任务列表文本
    report = window.TodoObj.get_report()
    # 访问粘贴板，将report复制在粘贴板内
    pyperclip.copy(report)

    # 避免卡死，必须在主线程更新UI
    window.TodoUpdateContent = todotext
    window.TodoUpdateFlag = True

def initLLMMethods(window):
    # 多线程执行对应操作
    window.btn_add.clicked.connect(lambda: threading.Thread(target=addMethod, args=(window,)).start())
    #window.btn_adjust.clicked.connect(lambda: adjustMethod(window))
    window.btn_adjust.clicked.connect(lambda: threading.Thread(target=adjustMethod, args=(window,)).start())
    #window.btn_format.clicked.connect(lambda: formatMethod(window))
    window.btn_format.clicked.connect(lambda: threading.Thread(target=formatMethod, args=(window,)).start())
    #window.btn_simple.clicked.connect(lambda: simpleMethod(window))
    window.btn_archive.clicked.connect(lambda: threading.Thread(target=archiveMethod, args=(window,)).start())
    window.btn_report.clicked.connect(lambda: threading.Thread(target=reportMethod, args=(window,)).start())
    window.btn_copyreport.clicked.connect(lambda: threading.Thread(target=copyreportMethod, args=(window,)).start())

def initRightClickMenu(window):
    # 定义菜单
    window.menu = QMenu(window)

    # 定义功能菜单项
    actions = {
        # "ernie":       QAction('文心一言', self, triggered=lambda: self.chatbox.show()),
        "simple_add":    QAction('添加一行', window, triggered=lambda: threading.Thread(target=addMethod, args=(window, "Origin")).start()),
        "add":           QAction('添加一行(LLM+Prompt)', window, triggered=lambda: threading.Thread(target=addMethod, args=(window, "LLM")).start()),
        "adjust":        QAction('调整任务(LLM+Prompt)', window, triggered=lambda: threading.Thread(target=adjustMethod, args=(window,)).start()),
        "format":        QAction('整理任务(LLM)', window, triggered=lambda: threading.Thread(target=formatMethod, args=(window,)).start()),
        "archive":       QAction('完成一项', window, triggered=lambda: threading.Thread(target=archiveMethod, args=(window,)).start()),
        "simple_report": QAction('生成报告', window, triggered=lambda: threading.Thread(target=reportMethod, args=(window, "pure",)).start()),
        "report":        QAction('生成报告(LLM)', window, triggered=lambda: threading.Thread(target=reportMethod, args=(window,)).start()),
        "copyreport":    QAction('复制报告', window, triggered=lambda: threading.Thread(target=copyreportMethod, args=(window,)).start()),
    }
    for key, value in actions.items():
        window.menu.addAction(value)

    # 添加分割线
    window.menu.addSeparator()

    # 定义常规菜单项
    actions = {
        "save":   QAction('保存', window, triggered=window.saveToDoList),
        "hide":   QAction('隐藏到托盘', window, triggered=lambda: window.setWindowOpacity(0)),
        "control":QAction('展开/折叠按钮', window,
                           triggered=lambda: window.controlBoxWidget.setVisible(not window.controlBoxWidget.isVisible())),
        "ernie":  QAction('打开文心一言', window, triggered=lambda: webbrowser.open("https://yiyan.baidu.com")),  # 打开网页
        "quit":   QAction('退出', window, triggered=window.quit),
    }
    for key, value in actions.items():
        window.menu.addAction(value)