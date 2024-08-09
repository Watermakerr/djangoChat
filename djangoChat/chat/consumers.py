import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from user.models import User

from django.core.exceptions import ObjectDoesNotExist

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if the user is anonymous
        if self.scope['user'].is_anonymous:
            # If the user is anonymous, we refuse the connection
            await self.close()
        else:
            self.room_name = self.scope['url_route']['kwargs']['user_id']
            self.room_group_name = f'chat_{self.room_name}'

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']

        await self.save_message(sender_id, self.room_group_name, message, receiver_id)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'receiver_id': receiver_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        receiver_id = event['receiver_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'receiver_id': receiver_id
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, sender_id, room_group_name, message, receiver_id):
        try:
            sender_user = User.objects.get(id=sender_id)
            receiver_user = User.objects.get(id=receiver_id)
            Message.objects.create(
                sender=sender_user,
                receiver=receiver_user,
                message=message
            )
        except ObjectDoesNotExist:
            print("User does not exist")