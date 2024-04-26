import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RealtimeOutput(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('output', self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard('output', self.channel_name)

    async def send_output(self, event):
        message=event['text']
        await self.send(message)