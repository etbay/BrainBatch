import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
@csrf_exempt
def get_canvas_courses(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            access_token = data.get('access_token')
            if not access_token:
                return JsonResponse({'error': 'Access token is required'}, status=400)
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get('https://canvas.instructure.com/api/v1/courses'
                                    '?enrollment_state=active', headers=headers)
            response.raise_for_status()
            courses = response.json()
            #print(response.text)
            return JsonResponse(courses, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)