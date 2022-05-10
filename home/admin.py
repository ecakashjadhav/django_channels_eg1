from django.contrib import admin
from .models import *

@admin.register(Chat)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['id','content','timestamp','group']

@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['id','name']

admin.site.register(Notifications)
admin.site.register(Students)