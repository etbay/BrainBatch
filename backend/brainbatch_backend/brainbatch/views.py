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
from django.db.models import Count
from .models import Group, GroupMembership, Message
from .serializers import GroupSerializer, MessageSerializer

def user_payload(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": getattr(user, "email", "") or "",
        "display_name": getattr(user, "first_name", "") or "",
    }

@api_view(["GET", "POST"])
def groups(request):
    if request.method == "GET":
        qs = Group.objects.filter(memberships__user=request.user).annotate(member_count=Count("memberships"))
        return Response(GroupSerializer(qs, many=True).data)
    name = (request.data.get("name") or "").strip()
    if not name:
        return Response({"error": "name is required"}, status=status.HTTP_400_BAD_REQUEST)
    g = Group.objects.create(name=name, created_by=request.user)
    GroupMembership.objects.create(user=request.user, group=g, role="owner")
    g.member_count = 1
    return Response(GroupSerializer(g).data, status=status.HTTP_201_CREATED)

def _require_membership(request, group_id):
    try:
        group = Group.objects.annotate(member_count=Count("memberships")).get(id=group_id)
    except Group.DoesNotExist:
        return None, Response({"error": "group not found"}, status=status.HTTP_404_NOT_FOUND)
    if not GroupMembership.objects.filter(group=group, user=request.user).exists():
        return None, Response({"error": "forbidden"}, status=status.HTTP_403_FORBIDDEN)
    return group, None

@api_view(["GET"])
def group_detail(request, group_id: int):
    group, error = _require_membership(request, group_id)
    if error:
        return error
    return Response(GroupSerializer(group).data)

@api_view(["GET", "POST"])
def group_messages(request, group_id: int):
    group, error = _require_membership(request, group_id)
    if error:
        return error

    if request.method == "POST":
        content = (request.data.get("content") or "").strip()
        if not content:
            return Response({"error": "content is required"}, status=status.HTTP_400_BAD_REQUEST)
        msg = Message.objects.create(group=group, user=request.user, content=content)
        return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)

    # GET: backscroll with ?before=<message_id>&limit=25
    try:
        limit = min(int(request.GET.get("limit", 20)), 100)
    except ValueError:
        limit = 20
    before = request.GET.get("before")
    qs = Message.objects.filter(group=group)
    if before:
        try:
            qs = qs.filter(id__lt=int(before))
        except ValueError:
            pass
    page_instances = list(qs.order_by("-id")[:limit])
    page_instances.reverse()  # return ascending for display
    data = MessageSerializer(page_instances, many=True).data
    if page_instances:
        first_id = page_instances[0].id
        has_more = Message.objects.filter(group=group, id__lt=first_id).exists()
        next_before = first_id
    else:
        has_more = False
        next_before = None
    return Response({"messages": data, "next_before": next_before, "has_more": has_more})

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