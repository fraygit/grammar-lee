1. create a gradio application
2. add a textbox name it "Claude API key"
3. once submitted, save the value to a a BrowserState, name it "grammar-lee-claude-api-key"
4. do not allow blank submission
5. show a two column panel.
6. left panel contains the following:
    1. Dropdown component, name it "Tone", add the following items in the dropdown
        1. Formal
        2. Natural
    2. Text area component, name it "Text".
    3. Once submitted, call the function "generate" passing the "Text" value and "Tone" value.
7. Create the function "generate", it will perform the following:
    1. use the anthropic sdk to do the following:
        1. use the model "claude-sonnet-4-20250514"
        2. max_token = 500
        3. initialise anthropic with the api key as the value from the BrowserState "grammar-lee-claude-api-key"
        3. set system to "you are an assistant expert that is an expert writer."
        4. set the user message to "reword and sound <Tone value>. '<Text value>'".
        5. call anthropic.Anthropic().messages.create
        6. display the output on the right panel.