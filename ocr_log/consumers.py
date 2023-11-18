import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .misspelling_check import word_check
from datetime import datetime

class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print(self.room_group_name)
        await self.accept()
        self.is_closed = False
        #asyncio.ensure_future(self.schedule_send_messages())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        self.is_closed = True

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "log_message", "message": message}
        )

    async def log_message(self, event):
        message = event["message"]
        region = word_check(message)
        timestamp = datetime.now().strftime("%m-%d %H:%M:%S")

        message_data = {
            'timestamp': timestamp,
            'message': region
        }

        await self.send(text_data=json.dumps(message_data))

    async def send_message(self):
        region = word_check("연자의 답 1증 로비")

        if region is not None:
            timestamp = datetime.now().strftime("%m-%d %H:%M:%S")
            message_data = {
                'timestamp': timestamp,
                'message': region
            }
            await self.send(text_data=json.dumps(message_data))

    async def schedule_send_messages(self):
        while not self.is_closed:
            await self.send_message()
            await asyncio.sleep(5)
