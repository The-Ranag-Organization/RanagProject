from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import requests

def gen(prompt):
    api_key = os.environ.get('HF_TOKEN', 'nil')
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {api_key}"}

    prompt = prompt

    params = {
        "max_new_tokens": 256,
        "temperature": 0.3,
        "top_p": 0.9,
        "do_sample": False
    }

    pload = {
        "inputs": prompt,
        "parameters": params
    }

    response = requests.post(API_URL, headers=headers, json=pload)

    if response.status_code == 200:
        resp = response.json()
        if isinstance(resp, list) and len(resp) > 0:
            generated = resp[0].get('generated_text', '')
            if generated.startswith(prompt):
                return generated[generated.find("[/INST]") + 7:].strip()
            return generated
        return str(resp)
    else:
        return f"Error: {response.status_code}"


@csrf_exempt
def process_prompt(request):
    if request.method == "POST":
        try:

            body = json.loads(request.body)

            promptbody = body.get("prompt", "")

            aigen = gen(promptbody)

            return JsonResponse({"generated": aigen})

        except json.JSONDecodeError:
            return JsonResponse({"error": "There was a fatal error while decoding json."}, status=400)
    else:
        return JsonResponse({"error": "GET is not an allowed method! Use POST instead."}, status=405)
