from django.urls import path
from .views import Index, get_chat_messages, newChat, get_doctors
app_name = 'messaging'


urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('new-chat/<int:sender>/<int:receiver>/', newChat, name='new-chat'),
    path('get_doctors/', get_doctors, name='get_doctors'),
    path("chats/<int:chat_id>/messages/", get_chat_messages, name="get_chat_messages"),
]
