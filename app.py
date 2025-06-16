import gradio as gr
from anthropic import Anthropic

# Util for BrowserState (Gradio 4.x)
# Removed save_api_key; browser localStorage will be used via JS injection

def generate(api_key, text, tone):
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
    with gr.Blocks() as demo:
        gr.HTML('''
        <script>
        // On page load, set the API key textbox from localStorage
        window.addEventListener('DOMContentLoaded', function() {
            const apiBox = document.querySelector('input[type="password"][aria-label="Claude API key"]');
            if (apiBox && localStorage.getItem('grammar-lee-claude-api-key')) {
                apiBox.value = localStorage.getItem('grammar-lee-claude-api-key');
            }
            // Save to localStorage on change
            if (apiBox) {
                apiBox.addEventListener('change', function() {
                    localStorage.setItem('grammar-lee-claude-api-key', apiBox.value);
                });
            }
        });
        </script>
        ''')
        with gr.Row():
            api_key_box = gr.Textbox(label="Claude API key", type="password")
        with gr.Row():
            with gr.Column():
                tone = gr.Dropdown(["Formal", "Natural"], label="Tone")
                text = gr.TextArea(label="Text")
                submit_btn = gr.Button("Generate")
            with gr.Column():
                output = gr.Markdown()
        submit_btn.click(fn=generate, inputs=[api_key_box, text, tone], outputs=output)
    return demo

if __name__ == "__main__":
    build_ui().launch()
