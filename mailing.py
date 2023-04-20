import asyncio
import random

from pyrogram import Client
from pyrogram import types

from pyrogram.errors.exceptions.bad_request_400 import ChatInvalid, ChatAdminRequired, ChatIdEmpty, ChatIdInvalid

from db_controllers.user_db import Users

from loguru import logger
import hashlib


class Mailing:
	@staticmethod
	async def mailing_by_file(client: Client, message: types.Message):
		d = await Users.get_user(message.from_user.id)
		__id = hashlib.sha256(str(message.from_user.id).encode()).hexdigest()

		user = Client(
			f"user_{__id}",
			api_id=d['api_id'], api_hash=d['api_hash'],
		)

		user_data = []
		with open(f'data/temp/{__id}.txt', 'rw') as file:
			while True:
				chat = file.readline()

	@staticmethod
	async def mailing_to_everyone(client: Client, message: types.Message):
		d = await Users.get_user(message.from_user.id)
		__id = hashlib.sha256(str(message.from_user.id).encode()).hexdigest()

		user = Client(
			f"user_{__id}",
			api_id=d['API_ID'], api_hash=d['API_HASH'],
		)
		await user.start()

		async for dialog in user.get_dialogs():
			try:
				for mes in d['messages']:
					await user.forward_messages(chat_id=dialog.chat.id, from_chat_id=message.chat.id, message_ids=mes)
			except (ChatInvalid, ChatAdminRequired, ChatIdEmpty, ChatIdInvalid) as err:
				logger.error(err)
				await client.send_message(
					message.from_user.id,
					text=f'При отвправке сообщения в чат id: {dialog.chat.id} произошла ошибка'
				)
				continue
			else:
				await client.send_message(
					message.from_user.id,
					text=f'Отправка сообщения в чат id: {dialog.chat.id} произведена успешно'
				)
			if len(d['interval']) == 2:
				await asyncio.sleep(random.randint(d['interval'][0], d['interval'][1])*60)
			elif len(d['interval']) == 1:
				await asyncio.sleep(d['interval'][0] * 60)

		await user.stop()
