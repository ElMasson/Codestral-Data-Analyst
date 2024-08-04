from mistralai.client import MistralClient
from dotenv import load_dotenv
import os
from src.utils import match_code_block

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL_NAME = "codestral-latest"

client = MistralClient(api_key=MISTRAL_API_KEY)

def describe_data(file_path):
    DESCRIBE_PROMPT = f"""You're a python data analysist that has for goal to describe the data provided. You are given tasks to create Python code to solve them.

    Information about the dataset:
    - It's in the {file_path}  file

    - The answer is the list of columns for each sheets in the following format
        -Sheet name
            -Column name, column type

    Generally, you follow these rules:
    - ALWAYS RESPOND ONLY WITH CODE IN CODE BLOCK LIKE THIS:
    ```python
    [code]
    ```
    - the python code runs in jupyter notebook.
    - The output is code that generates the description
    - The output is code that generates the description and stores the full description in an object called descr in a string format and make it available for the next function
    - The code ends with a return descr
    """

    desc_question = "Describe the file provided"

    description = client.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": DESCRIBE_PROMPT},
            {"role": "user", "content": desc_question}
        ],
    )
    description_message = description.choices[0].message

    return match_code_block(description_message.content)
