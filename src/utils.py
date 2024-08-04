import re

def match_code_block(llm_response):
    pattern = re.compile(r'```python\n(.*?)\n```', re.DOTALL)
    match = pattern.search(llm_response)
    if match:
        return match.group(1)
    return ""
