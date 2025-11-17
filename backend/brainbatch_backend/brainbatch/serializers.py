from rest_framework import serializers
from .models import Group, Message

class GroupSerializer(serializers.ModelSerializer):
    member_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Group
        fields = ("id", "name", "created_by", "created_at", "member_count")
        read_only_fields = ("id", "created_by", "created_at", "member_count")

class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Message
        fields = ("id", "group", "user", "username", "content", "created_at")
        read_only_fields = ("id", "group", "user", "username", "created_at")