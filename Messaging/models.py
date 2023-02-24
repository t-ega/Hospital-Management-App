from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='chat_sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='chat_received_messages', on_delete=models.CASCADE)
    messages = models.ManyToManyField('Message', related_name='chat_messages')
    timestamp = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='chat', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'timestamp'
