import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hospital_Management_App.settings")
django.setup()
from .models import Message, Chat


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'receiver': receiver,
            }
        )

        # create a new message a save it
        message = Message.objects.create(content=message, sender_id=sender, receiver_id=receiver,
                                         chat_id=self.room_name)
        # associate that message with a chat
        chat = Chat.objects.get(id=self.room_name)

        chat.messages.add(message)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'sender': sender,
            'content': message,
            'timestamp': datetime.datetime.now().strftime("%I:%M %p | %b %d")
        }))


