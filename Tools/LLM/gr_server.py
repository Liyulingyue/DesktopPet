from gradio_client import Client

class GradioClass(object):
    def __init__(self, url="http://116.62.10.217:8890/"):
        self.chat_history = []

        self.client = Client(url)


    def chat(self, prompt, role='user'):
        result = self.client.predict(
            in_text=prompt,
            api_name="/fn_get_response"
        )
        return result

    def get_llm_answer(self, prompt):
        result = self.client.predict(
            in_text=prompt,
            api_name="/fn_get_response"
        )
        return result
