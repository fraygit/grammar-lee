import gradio as gr
from anthropic import Anthropic

# Util for BrowserState (Gradio 4.x)
# Removed save_api_key; browser localStorage will be used via JS injection

# The generate function now expects the API key to be provided via state
# (Gradio v4: gr.BrowserState; fallback to gr.State for v3)
def generate(text, tone, api_key_state):
    api_key = api_key_state  # This comes from BrowserState/State
    if not api_key:
        return "Please enter your Claude API key."
    client = Anthropic(api_key=api_key)
    system = "you are an assistant expert that is an expert writer."
    user_message = f"reword and sound {tone}. '{text}'"
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            system=system,
            messages=[{"role": "user", "content": user_message}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: {e}"

def build_ui():
    # Use BrowserState if available (Gradio v4+), otherwise fallback to State
    try:
        BrowserState = gr.BrowserState
    except AttributeError:
        BrowserState = gr.State

    with gr.Blocks() as demo:

        api_key_state = BrowserState()
        with gr.Row() as api_row:
            api_key_box = gr.Textbox(label="Claude API key", type="password", visible=True)
            set_api_btn = gr.Button("Set API Key", visible=True)
        with gr.Row():
            with gr.Column():
                tone = gr.Dropdown(["Formal", "Natural"], label="Tone")
                text = gr.TextArea(label="Text")
                submit_btn = gr.Button("Generate")
            with gr.Column():
                output = gr.Markdown()
        # Set API key in state when button is clicked
        set_api_btn.click(lambda k: k.strip(), inputs=api_key_box, outputs=api_key_state)

        # Hide API key textbox and button if API key is already set in state
        def toggle_api_row(api_key):
            visible = not bool(api_key)
            return gr.update(visible=visible), gr.update(visible=visible)
        api_key_state.change(toggle_api_row, inputs=api_key_state, outputs=[api_key_box, set_api_btn])

        # Only allow generate if API key is set in state
        submit_btn.click(
            fn=generate,
            inputs=[text, tone, api_key_state],
            outputs=output
        )
    return demo

if __name__ == "__main__":
    build_ui().launch()
