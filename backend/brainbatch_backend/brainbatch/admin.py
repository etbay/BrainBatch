from django.contrib import admin
from .models import Group, GroupMembership, Message

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by", "created_at")

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "group", "role", "joined_at")
    list_filter = ("role",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "group", "user", "created_at")
    search_fields = ("content",)
