from django.contrib import admin
from .models import Chat, Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('content', 'sender', 'receiver', 'chat')


admin.site.register(Chat)
admin.site.register(Message, MessageAdmin)

