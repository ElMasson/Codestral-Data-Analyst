from mistralai.client import MistralClient
from dotenv import load_dotenv
import os
from src.describe_data import describe_data
from src.utils import match_code_block
import json


load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL_NAME = "codestral-latest"

client = MistralClient(api_key=MISTRAL_API_KEY)

def store_exec_result(code):
    # Create an empty dictionary to store the results
    desc_data = {}
    # Execute the code
    exec(code, globals(), desc_data)
    # Convert the 'desc_data' part of the results to a JSON string
    str_desc_data = json.dumps(desc_data.get('descr', {}))
    # Return the 'desc_data' part of the results as a JSON string
    return str_desc_data

def analyze_data(file_path, user_question):
    # Étape 1 : Générer le code pour la description
    description_code = describe_data(file_path)
    print("Description Code Generated!!!"+description_code)

    desc_data = store_exec_result(description_code)

    print("Youhou - Description Data Captured - Go to APT!!!")


    ANALYSIS_PROMPT_TEMPLATE = f"""You're a python data analysist that has for goal to analyse sales, profit, costs, transations and customer behavior in the superstore supermarkets. 
    You are given tasks to create Python code to create a plot ton answer the user queston.

    Information about the Superstore dataset:
    - It's in the {file_path}  file
    - It has following sheets and columns {desc_data}

    Generally, you follow these rules:
    - ALWAYS RESPOND ONLY WITH CODE IN CODE BLOCK LIKE THIS:
    ```python
    [code]
    ```
    - the python code runs in jupyter notebook.
    - Forecast are done using prophet
    - The result of the code is always a plot
    - every time you generate python, the code is executed in a separate cell. it's okay to multiple calls to `execute_python`.
    - display visualizations using matplotlib or any other visualization library directly in the notebook. don't worry about saving the visualizations to a file.
    - you have access to the internet and can make api requests.
    - you also have access to the filesystem and can read/write files.
    - Check in requirements file if the needed packages are installed. If not you can install any pip package (if it exists) if you need to be running `!pip install [package]`.
    - you can install any pip package (if it exists) if you need to be running `!pip install [package]`. The usual packages for data analysis are already preinstalled though.
    - you can run any python code you want, everything is running in a secure sandbox environment
    """

    analysis_prompt = ANALYSIS_PROMPT_TEMPLATE.format(desc_data=desc_data)
    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": analysis_prompt},
            {"role": "user", "content": user_question}
        ],
    )
    response_message = response.choices[0].message

    return match_code_block(response_message.content)