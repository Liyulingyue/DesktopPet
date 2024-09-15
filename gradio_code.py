import gradio as gr
import yaml

from Tools.LLM.glm3 import GLM3Class

config_dict = yaml.safe_load(
    open('Source/config.yaml')
)

llm = GLM3Class(config_dict.get("GLM3Directory", ""))

def fn_get_response(in_text):
    result = llm.get_llm_answer(in_text)
    return result

with gr.Blocks() as demo:
    in_text = gr.Textbox()
    out_text = gr.Textbox()
    btn = gr.Button("Submit")

    btn.click(fn=fn_get_response, inputs=in_text, outputs=out_text)

demo.launch(server_name="0.0.0.0", server_port=15001)

