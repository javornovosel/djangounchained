import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
	def connect(self):
		self.room_group_name = 'test'

		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
			)
		self.accept()


	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type':'chat_message',
				'message':message
			}
		)

	def chat_message(self, event):
		message = event['message']
		self.send(text_data=json.dumps({
			'type':'chat',
			'message':message
			}))

class ChatroomConsumer(AsyncWebsocketConsumer):
	async def connect(self):#tu dodati username
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = f'chat_{self.room_name}'

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()

		
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type':'tester_message',
				'tester':'hello world',
				#'username':username
			}
		)

	async def tester_message(self, event):
		tester = event['tester']

		await self.send(text_data=json.dumps({
			'tester':tester
		}))

	async def disconnect(self, close_code):

		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message= text_data_json['message']
		username = text_data_json['username']

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type':'chatroom_message',
				'message':message,
				'username':username
			}
		)

	async def chatroom_message(self, event):
		message = event['message']
		username = event['username']

		await self.send(text_data=json.dumps(
			{
			'message':message,
			'username':username
		}))



#u htmlu za draft, mogu stvarati <img za svaku kartu sa imenom i rarityem skupa kao id>, chat bi trebal biti sa strane 