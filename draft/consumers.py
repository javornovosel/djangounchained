import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio 
from box.methods import get_random_packs
from asgiref.sync import async_to_sync, sync_to_async


#u htmlu za draft, mogu stvarati <img za svaku kartu sa imenom i rarityem skupa kao id>, chat bi trebal biti sa strane 

class ChatroomConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        handlers = {
            'chatroom_message': self.handle_chatroom_message,
            'draft_choice': self.handle_draft_choice,
            'get_pack' : self.handle_get_pack

        }

        handler = handlers.get(text_data_json['type'], self.handle_unknown_message)
        await handler(text_data_json)

    async def handle_chatroom_message(self, data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': data['message'],
                'username': data['username']
            }
        )

    async def handle_draft_choice(self, data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'draft_choice',
                'username' : data['username'],
                'drafted_card_id' : data['drafted_card_id'],
                'drafted_card_name' : data['drafted_card_name'],
                'drafted_card_image' :  data['drafted_card_image']

            }
        )

    async def handle_get_pack(self, data):
    	pack_list = await sync_to_async(get_random_packs)('Romance Dawn', 1, True)
    	await self.channel_layer.group_send(
   			self.room_group_name,
   			{
   				'type':'get_pack',
   				'card_list':pack_list[0]
   			})


    async def handle_unknown_message(self, data):
        pass

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'type': 'chatroom_message',
            'message': message,
            'username': username
        }))

    async def draft_choice(self, event):
        username = event['username']
        drafted_card_id = event['drafted_card_id']
        drafted_card_name = event['drafted_card_name']
        drafted_card_image = event['drafted_card_image']

        await self.send(text_data=json.dumps({
            'type' : 'draft_choice',
            'username' : username,
            'drafted_card_id' : drafted_card_id,
            'drafted_card_name' : drafted_card_name,
            'drafted_card_image' : drafted_card_image
        }))

    async def get_pack(self, event):
    	card_list = event['card_list']

    	await self.send(text_data=json.dumps({
    		'type' : 'get_pack',
    		'card_list' : card_list
    		}))
