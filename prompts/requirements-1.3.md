1. specify the gradio version to be used to be gradio==5.34.0.
2. in the app.py file, do the following:
    1. remove the JS injection code to store the API key in the browser.
    2. update the generate function to use the browser state variable to store the API key.
    3. update the generate function to expect the API key from the browser state variable.
    4. hide the API key textbox and Set API key button if the API key is already set in the browser state variable.