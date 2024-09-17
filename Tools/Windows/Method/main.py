import threading

def addMethod(window):
    todotext = window.ToDoList.toPlainText() # 获取界面上的任务列表文本
    user_input = window.TextInput.text() # 获取用户输入的文本

    # 如果用户输入的文本不为空，则执行以下操作
    if not user_input.strip() == '':
        # task_text = user_input
        prompt = f"""
请根据用户需求，对需求消耗时间进行规划，并输出结果。
用户的需求是：{user_input}
请以json格式输出。输出内容是一个list[字典]，字典内容如下：
[{'{'}
    'Time': int，取值0-10，需要消耗的时间，单位为小时，
    'Task': str，具体的任务内容，
    'Priority': int，取值为0-10，任务的优先级，越高越重要
{'}'}]
如果任务需要拆分，则进行拆分，输出list中包含各个步骤。如果任务无需拆分，则输出仅含一个成员的list。
"""
        llm_result = window.llm.get_llm_json_answer(prompt)
        print(llm_result)
        task_text = ""
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
        prompt = f"""根据{user_input}，继续对{todotext}进行调整
        ## Goals
        - 根据日程优先级确定事件先后顺序
        - 判断日程的合理性
        - 拆解日程并合理分配时间
        
        ## Constrains
        - 日程安排必须简洁明了，重点突出。
        - 日程安排长度应控制在 50 字以内。
        - 输出结果100字内必须仅为日程安排内容
        - 不包含其他多余信息。
        
        ## Skills
        - 根据日程优先级确定事件先后顺序
        - 判断日程的合理性
        - 拆解日程并合理分配时间
        
        ## Output
        - 输出格式: 格式为列表
        - 每个日程为一行
        - 按照优先级先后排列
        - 显示预计完成时间
        
        ## Workflow
        1. 读取并理解给定的日程安排内容。
        2. 提取需求的主要内容，优先级和时间安排。
        3. 生成简明扼要的日程安排。
        
        """
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

    prompt = (f"""请重复：{todotext},并以案例的形式输出，要求内容简洁，没有冗余。一个日程为一行，
    - 不需要输出思考过程
    - 只需要输出结果
    - 不需要输出“根据您的需求”开头的内容
    - 不需要输出其他注意等提示
    - 不需要输出带"（"或带"）"的内容
    - 不需要输出空白行
    不允许输出信息中含有时间段。严格按照以下格式：
    - 1h 八段锦
    - 2h 书法
    - 0.5 买菜
    """)
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
    #window.btn_adjust.clicked.connect(lambda: adjustMethod(window))
    window.btn_adjust.clicked.connect(lambda: threading.Thread(target=adjustMethod, args=(window,)).start())
    #window.btn_format.clicked.connect(lambda: formatMethod(window))
    window.btn_format.clicked.connect(lambda: threading.Thread(target=formatMethod, args=(window,)).start())
    #window.btn_simple.clicked.connect(lambda: simpleMethod(window))
    window.btn_simple.clicked.connect(lambda: threading.Thread(target=simpleMethod, args=(window,)).start())