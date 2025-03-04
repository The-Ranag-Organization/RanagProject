from django.shortcuts import render

def home(request):
    return render(request, 'sitefiles/index.html')

def download(request):
    return render(request, 'sitefiles/download.html')

from django.http import JsonResponse
import json
import requests
import os

def process_prompt(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            promptbody = body.get("prompt", "")
            
            # Usando a mesma lógica que está em api/ranagapi/api/views.py
            api_key = os.environ.get('HF_TOKEN', 'nil')
            API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            params = {
                "max_new_tokens": 256,
                "temperature": 0.3,
                "top_p": 0.9,
                "do_sample": False
            }
            
            pload = {
                "inputs": promptbody,
                "parameters": params
            }
            
            response = requests.post(API_URL, headers=headers, json=pload)
            
            if response.status_code == 200:
                resp = response.json()
                if isinstance(resp, list) and len(resp) > 0:
                    generated = resp[0].get('generated_text', '')
                    if generated.startswith(promptbody):
                        result = generated[generated.find("[/INST]") + 7:].strip()
                    else:
                        result = generated
                else:
                    result = str(resp)
            else:
                result = f"Error: {response.status_code}"
                
            return JsonResponse({"generated": result})
        except json.JSONDecodeError:
            return JsonResponse({"error": "There was a fatal error while decoding json."}, status=400)
    else:
        return JsonResponse({"error": "GET is not an allowed method! Use POST instead."}, status=405)
