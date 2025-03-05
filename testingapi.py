import requests
import json

def gen():
    API_URL = "https://api-ranagproject.onrender.com/process/"

    data = {
        "prompt": '<s>[INST] You are a friendly chatbot that responds with kindness and positivity. '[
                  'Always make sure to be polite and engaging in your conversations. '
                  'Your tone should be warm and approachable. '
                  "Respond in English and always end with the phrase 'Hello, how you are?' [/INST]"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            resp = response.json()
            return resp.get("generated", "Error: 'generated' key not found in response")
        else:
            return f"Error: {response.status_code}\n{response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request Error: {str(e)}"


print(gen())