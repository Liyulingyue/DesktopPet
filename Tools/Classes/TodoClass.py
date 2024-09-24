import datetime
import os

import yaml

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)


class TodoClass(object):
    def __init__(self):
        super().__init__()

        # 从配置中读取待办事项列表
        if os.path.exists(config_dict["TodoFile"]):
            with open(config_dict["TodoFile"], "r", encoding="utf8") as f:
                self.todo_list = [line.replace("\n", "") for line in f.readlines() if line.strip() != ""]
                # self.ToDoList.setPlainText("".join(todo_list))
        else:
            self.todo_list = []

        self.archive_list = []
        self.daily_report = ""

    def get_plaintext(self):
        return '\n'.join(self.todo_list)

    def update_todolist(self, new_todo_list):
        if isinstance(new_todo_list, str):
            new_todo_list = [line for line in new_todo_list.split("\n") if line.strip()!=""]
        self.todo_list = new_todo_list

    def archive(self, number=1):
        # 当前仅支持number=1
        if number != 1:
            raise NotImplementedError

        # archive_list = []
        for i in range(min(number, len(self.todo_list))):
            # archive i
            # print(f"Archiving {self.todo_list[i]}")
            self.archive_list.append({'content': self.todo_list[i], 'time': datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")})
            del self.todo_list[i]

        # print(f"Archived {archive_list}")

    def save(self):
        # 检查配置文件是否存在，不存在则创建
        for key in ["TodoFile", "TodoArchive"]:
            if not os.path.exists(config_dict[key]):
                # 创建文件夹
                dir_path = os.path.dirname(config_dict[key])
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

        # 记录当前的代办事项
        with open(config_dict["TodoFile"], "w", encoding="utf8") as f:
            f.write(self.get_plaintext())

        # 记录已归档的代办事项
        with open(config_dict["TodoArchive"], "a", encoding="utf8") as f:
            for item in self.archive_list:
                f.write(f"{item['time']} {item['content']}\n")

    def get_today_archives(self):
        today = datetime.date.today()
        archives = []
        # 从历史记录中读取今天的归档
        with open(config_dict["TodoArchive"], "r", encoding="utf8") as f:
            lines = f.readlines()
            for line in reversed(lines):
                try:
                    date = datetime.datetime.strptime(line[:19], "%Y-%m-%d-%H-%M-%S").date()
                    if date == today:
                        archives.append(line[20:].strip())
                    else:
                        break
                except ValueError:
                    pass
        # 从当前记录中读取今天的归档
        for item in self.archive_list:
            date = datetime.datetime.strptime(item['time'], "%Y-%m-%d-%H-%M-%S").date()
            if date == today:
                archives.append(item['content'])
        return "\n".join(archives)

    def generate_report(self, llm):
        archive_text = self.get_today_archives()
        prompt = f"""
        请根据用户今天完成的工作内容：{archive_text}，生成当日的工作总结。
        请以json格式输出，字典内容如下：
        {'{'}
            Report: str, 当日的工作总结
        {'}'}
        """
        report = llm.get_llm_json_answer(prompt)
        try:
            report = report['Report']
        except:
            report = "生成失败"

        self.daily_report = report

        return report

    def get_report(self):
        return self.daily_report