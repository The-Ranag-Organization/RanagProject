from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def process_prompt(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')

            # Simple response for testing
            generated_text = "This is a test response from the API: " + prompt[:50] + "..."

            return JsonResponse({'generated': generated_text})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'GET':
        # Adding GET method support for testing
        return JsonResponse({'generated': 'This is a test response from GET request'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)