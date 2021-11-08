import json
from django.db.models import Count
from .models import *
from .views import find_username
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async




class SetOnline(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        print(1243432423423432423423423423423432)
        await self.update_user_status(user, True)
        await self.accept()

    @database_sync_to_async
    def update_user_status(self, user, status):
        user_profile.objects.filter(user=user).update(online=status)

    async def disconnect(self, close_code):
        user = self.scope['user']
        await self.update_user_status(user, False)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from_user = self.scope['user']
        to_user_id = self.scope['url_route']['kwargs']['to_user']
        to_user = await self.get_user(to_user_id)
        users = [from_user, to_user]
        try:
            self.current_chat = await self.get_current_chat(users)
            self.chat_group_name = 'dialog' + str(self.current_chat.id)
        except Exception as e:
            self.current_chat = await self.create_new_chat(users)
            self.chat_group_name = 'dialog' + str(self.current_chat.id)


        count = getattr(self.channel_layer, self.chat_group_name, 0)
        if not count:
            setattr(self.channel_layer, self.chat_group_name, 1)
        else:
            setattr(self.channel_layer, self.chat_group_name, count + 1)


        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        print(self.chat_group_name)
        await self.accept()


    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type'):
            target_messages = data['messages_id']
            try:
                await self.read_messages(self.current_chat, target_messages)
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    {
                        'type': 'new_message',
                        'message': {
                            'type': 'read_message',
                            'attempt': True,
                            'readed_messages': target_messages
                        }
                    })
            except Exception as e:
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    {
                        'type': 'new_message',
                        'message': {
                            'type': 'read_message',
                            'attempt': False,

                        }
                    })
        else:
            from_user = self.scope['user']
            to_user = data['to_user']
            text = str(data['text'])
            msg_id = data['message_id']
            message = await self.create_new_message(from_user, text, self.current_chat, msg_id)


            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'new_message',
                    'message': {
                        'to_user': {
                            'id': to_user,
                            'msg': {
                                'msg_id': message.id,
                                'text': message.text,
                            },
                        },
                        'user': {
                            'is_readed': message.isReaded
                        }
                    }
                })

    async def new_message(self, event):
        message = event['message']
        await self.send(
            text_data=json.dumps(
                {
                    'message': message
                }
            )
        )


    @database_sync_to_async
    def read_messages(self, chat, msg):
        for m in msg:
            mesg = chat.messages.get(id=m)
            mesg.isReaded = True
            mesg.save()

    @database_sync_to_async
    def create_new_message(self, from_user, text, current_chat, msg_id):
        users_count = getattr(self.channel_layer, self.chat_group_name)
        msg = message(id=msg_id, user=from_user, text=find_username(text), chat=current_chat, isReaded=True if users_count == 2 else False)
        msg.save()
        print('chat -------- ',current_chat, timezone.now)
        current_chat.data = timezone.now()
        current_chat.save()
        return msg

    @database_sync_to_async
    def create_new_chat(self, users):
        current_chat = chat.objects.create()
        current_chat.user.add(users[0])
        current_chat.user.add(users[1])
        current_chat.save()
        return current_chat


    @database_sync_to_async
    def get_user(self, user_id):
        user = User.objects.get(id=user_id)
        return user

    @database_sync_to_async
    def get_current_chat(self, users):
        current_chat = chat.objects.filter(user__in=users).annotate(num_user=Count('user')).filter(num_user=len(users))[
            0]
        return current_chat

    async def disconnect(self, close_code):
        count = getattr(self.channel_layer, self.chat_group_name, 0)
        setattr(self.channel_layer, self.chat_group_name, count - 1)
        if count == 1:
            delattr(self.channel_layer, self.chat_group_name)
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        self.notific_group_name = 'notificate' + str(user.id)

        await self.channel_layer.group_add(
            self.notific_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.notific_group_name,
             self.channel_name
        )

    async def send_notif(self, event):
        msg = event['text']
        await self.send(text_data=json.dumps(msg))






