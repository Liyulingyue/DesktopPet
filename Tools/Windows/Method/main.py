import threading

def addMethod(window):
    todotext = window.ToDoList.toPlainText() # 获取界面上的任务列表文本
    user_input = window.TextInput.text() # 获取用户输入的文本

    # 如果用户输入的文本不为空，则执行以下操作
    if not user_input.strip() == '':
        # task_text = user_input
        prompt = f"请重复：{user_input}"
        task_text = window.llm.chat(prompt)
    else:
        task_text = ""

    # 更新任务列表文本
    todotext = window.ToDoList.toPlainText()  # 获取界面上的任务列表文本

    if not todotext.endswith('\n'):
        todotext += '\n'
    todotext += task_text

    # 避免卡死，必须在主线程更新UI
    window.TodoUpdateContent = todotext
    window.TodoUpdateFlag = True

def adjustMethod(window):
    todotext = window.ToDoList.toPlainText() # 获取界面上的任务列表文本
    user_input = window.TextInput.text() # 获取用户输入的文本

    # 如果用户输入的文本不为空，则执行以下操作
    if not user_input.strip() == '':
        # task_text = user_input
        prompt = f"根据{user_input}，对{todotext}进行调整"
        task_text = window.llm.chat(prompt)
    else:
        task_text = todotext

    # 更新任务列表文本
    todotext = task_text

    # 避免卡死，必须在主线程更新UI
    window.TodoUpdateContent = todotext
    window.TodoUpdateFlag = True


def formatMethod(window):
    todotext = window.ToDoList.toPlainText() # 获取界面上的任务列表文本
    user_input = window.TextInput.text() # 获取用户输入的文本

    prompt = f"请重复：{todotext}"
    task_text = window.llm.chat(prompt)

    # 更新任务列表文本
    todotext = task_text

    # 避免卡死，必须在主线程更新UI
    window.TodoUpdateContent = todotext
    window.TodoUpdateFlag = True


def simpleMethod(window):
    todotext = window.ToDoList.toPlainText() # 获取界面上的任务列表文本

    # 删除todotext第一行（第一个换行符即之前的内容删除）
    if todotext.find("\n") != -1:
        todotext = todotext[todotext.find("\n") + 1:]
    else:
        todotext = ''

    # 避免卡死，必须在主线程更新UI
    window.TodoUpdateContent = todotext
    window.TodoUpdateFlag = True

def initLLMMethods(window):
    # 多线程执行对应操作
    window.btn_add.clicked.connect(lambda: threading.Thread(target=addMethod, args=(window,)).start())
    window.btn_adjust.clicked.connect(lambda: adjustMethod(window))
    window.btn_format.clicked.connect(lambda: formatMethod(window))
    window.btn_simple.clicked.connect(lambda: simpleMethod(window))