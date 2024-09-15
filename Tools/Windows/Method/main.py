import threading

def addMethod(window):
    todotext = window.ToDoList.toPlainText() # 获取界面上的任务列表文本
    user_input = window.TextInput.text() # 获取用户输入的文本

    # 如果用户输入的文本不为空，则执行以下操作
    if not user_input.strip() == '':
        # task_text = user_input
        prompt = f"""# Role: ToDoList
你的角色是一个日程计划软件TodoList。接下来是你的角色设定
## Goals
- 维护一个日程计划表，根据用户提供的信息规划日程安排。结合用户反馈对日程内容进行调整。

## Constrains
- 日程安排必须简洁明了，重点突出。
- 日程安排长度应控制在 150 字以内。
- 输出结果必须仅为日程安排内容，不包含其他多余信息。
- 不需要输出思考过程
- 只需要输出结果
- 不需要输出“根据您的需求”开头的内容
- 不需要输出其他注意等提示
- 不需要输出带"（"或带"）"的内容
- 不需要输出空白行

## Skills
- 根据日程优先级排序
- 判断日程的合理性
- 拆解日程并合理分配时间

## Output
- 输出格式: 每个日程为一行
- 按照优先级先后排列
- 显示需要的时长，不需要输出所需的时间区间
- 不允许输出思考过程
- 只输出规划的日程计划,其他信息文字不需要输出
- 不允许输出信息中含有时间段
- 不允许输出信息中含有括号

输出内容严格按照以下格式：
- 1h 八段锦
- 2h 书法
- 0.5 买菜
只允许输出以上带格式内容，不需要其他信息提示。
后续我会提供信息：{user_input}"""
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