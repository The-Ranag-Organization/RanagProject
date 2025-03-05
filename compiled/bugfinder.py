# BETA 0.5.6
import requests 
import json

def finder(tofind):
    API_URL = "https://api-ranagproject.onrender.com/process/"
    prompt = f"<s>[INST] You are a Code Bug Finder. Your task is to analyze the provided code, identify any syntax or logical errors, and suggest the correct version. If you don't find any bug just say NIL.\n\n"

    prompt += "For each mistake, output it in the following format:\n"
    prompt += "£wrong_snippet£—¥correct_snippet¥\n\n"

    prompt += "Rules:\n"
    prompt += "1. Each error should be enclosed in `£` and `¥` as shown.\n"
    prompt += "2. Do NOT include nested corrections inside another correction.\n"
    prompt += "3. If multiple errors exist, list them separately in new lines.\n"
    prompt += "4. Preserve the original indentation and structure as much as possible.\n\n"

    prompt += "Example:\n\n"
    prompt += "Input code:\n\n"
    prompt += "print(hello world)\n"
    prompt += "variable = 10;\n\n"
    prompt += "def hello:\n"
    prompt += 'print(“hello!”)\n\n'

    prompt += "Expected output:\n\n"
    prompt += "£print(hello world)£—¥print(“hello world”)¥\n"
    prompt += "£def hello:£—¥def hello():¥\n\n"

    prompt += "Now, analyze the following code and return the corrected snippets:\n\n"
    prompt += f"{tofind}\n[/INST]"
    
    data = {"prompt": prompt}

    headers = {"Content-Type": "application/json"}

    response = requests.post(API_URL, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        resp = response.json()
        if 'generated' in resp:
            resp = resp['generated']
        return str(resp)
    else:
        return f"Error: {response.status_code}"

