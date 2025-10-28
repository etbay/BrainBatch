import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

def user_payload(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email or "",
        "display_name": user.first_name or "",
    }

@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def register(request):
    data = request.data or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    email = (data.get("email") or "").strip()
    display_name = (data.get("display_name") or data.get("displayname") or "").strip()

    if not username or not password:
        return Response({"error": "username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username__iexact=username).exists():
        return Response({"error": "username already taken"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    if display_name:
        user.first_name = display_name
        user.save()
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "user": user_payload(user)}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def login(request):
    data = request.data or {}
    username = data.get("username") or ""
    password = data.get("password") or ""
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "invalid login"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "user": user_payload(user)}, status=status.HTTP_200_OK)

@api_view(["GET"])
def me(request):
    return Response({"user": user_payload(request.user)})

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