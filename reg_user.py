from pyrogram import Client
from pyrogram import filters, types
from pyrogram.handlers import MessageHandler

from db_controllers.user_db import Users
from filters import Filters

from loguru import logger
import hashlib


class RegistrationHandler:
	def __init__(self, bot):
		bot.add_handler(
			MessageHandler(
				RegistrationHandler._help,
				filters=filters.command('help_reg')
			)
		)
		bot.add_handler(
			MessageHandler(
				RegistrationHandler.api_id,
				filters=filters.command('api_id')
			)
		)
		bot.add_handler(
			MessageHandler(
				RegistrationHandler.api_hash,
				filters=filters.command('api_hash')
			)
		)
		bot.add_handler(
			MessageHandler(
				RegistrationHandler.reg,
				filters=filters.command('reg')
			)
		)
		bot.add_handler(
			MessageHandler(
				RegistrationHandler.tel,
				filters=filters.command('tel') & Filters.reg_mode()
			)
		)
		bot.add_handler(
			MessageHandler(
				RegistrationHandler.contact,
				filters=filters.contact & Filters.reg_mode()
			)
		)
		bot.add_handler(
			MessageHandler(
				RegistrationHandler.code,
				filters=filters.command('code') & Filters.reg_mode()
			)
		)
		logger.info('\t-- RegistrationHandler initialized --')

	@staticmethod
	async def _help(client: Client, message: types.Message):
		text = f'''1. Для получения <b>api_id</b> и <b>api_hash</b> перейдите по ссылке
		https://core.telegram.org/api/obtaining_api_id
		2. Для записи <b>api_id</b> используй команду /api_id [Ваш api_id]
		3. Для записи <b>api_hash</b> используй команду /api_hash [Ваш api_hash]
		4. Используйте команду /reg
		5. Введите ваш номер телефона.
		6. Введите полученый код.'''
		await client.send_message(message.from_user.id, text=text)

	@staticmethod
	async def api_id(client: Client, message: types.Message):
		await Users.user_update_api_id(message.from_user.id, message.text.split()[1])
		text = f'Ваш <b>api_id</b>: <b>{message.text.split()[1]}</b>, пожалуйста, проверьте.'
		await client.send_message(message.from_user.id, text=text)

	@staticmethod
	async def api_hash(client: Client, message: types.Message):
		await Users.user_update_api_hash(message.from_user.id, message.text.split()[1])
		text = f'Ваш <b>api_hash</b>: <b>{message.text.split()[1]}</b>, пожалуйста, проверьте.'
		await client.send_message(message.from_user.id, text=text)

	@staticmethod
	async def reg(client: Client, message: types.Message):
		__id = hashlib.sha256(str(message.from_user.id).encode()).hexdigest()
		d = await Users.get_user(message.from_user.id)

		user_client = Client(
			f'sessions/user_{__id}',
			api_id=d['API_ID'],
			api_hash=d['API_HASH'],
			in_memory=True
		)
		await user_client.connect()

		await Users.user_update_reg_mode(message.from_user.id, True)
		session_string = ''
		if not d['phone'] is None:
			sCode = await user_client.send_code(d['phone'])
			await Users.user_update_sCode_hash(message.from_user.id, sCode.phone_code_hash)
			await client.send_message(
				message.from_user.id,
				text='Вам был отправлен код для завершения регистрации используй /code [Код]'
			)
			session_string = await user_client.export_session_string()
			await user_client.stop()

		if message.from_user.phone_number is None:
			await client.send_message(
				message.from_user.id,
				text=
				'Не могу получить ваш номер телефона, пожалуйста отправте контакт или используйте /tel [номер '
				'телефона в формате +7XXXXXXXXXX]'
			)
			await user_client.disconnect()

		else:
			sCode = await user_client.send_code(message.from_user.phone_number)
			await Users.user_update_sCode_hash(message.from_user.id, sCode.phone_code_hash)
			await client.send_message(
				message.from_user.id,
				text='Вам был отправлен код для завершения регистрации используй /code [Код]'
			)

			session_string = await user_client.export_session_string()
			await user_client.stop()

		with open(f'sessions/sessions_{__id}.txt', 'w') as file:
			file.write(str(session_string))


	@staticmethod
	async def tel(client: Client, message: types.Message):
		phone_number = message.text.split()[1]
		if phone_number[:2] == '+7' and phone_number[2:].isdigit() and len(phone_number[2:]) == 10:
			await Users.user_update_phone(message.from_user.id, phone_number)
			await client.send_message(
				message.from_user.id,
				text=
				'Номер был записан'
			)
		else:
			await client.send_message(
				message.from_user.id,
				text=
				'Испльзуйте /reg +7XXXXXXXXXX'
			)

	@staticmethod
	async def contact(client: Client, message: types.Message):
		phone_number = message.contact.phone_number
		if not phone_number is None:
			await Users.user_update_phone(message.from_user.id, phone_number)
			await client.send_message(
				message.from_user.id,
				text=
				'Номер был записан'
			)
		else:
			await client.send_message(
				message.from_user.id,
				text=
				'Испльзуйте /reg +7XXXXXXXXXX'
			)

	@staticmethod
	async def code(client: Client, message: types.Message):
		__id = hashlib.sha256(str(message.from_user.id).encode()).hexdigest()

		d = await Users.get_user(message.from_user.id)
		with open(f'sessions/sessions_{__id}.txt', 'r') as file:
			session_string = file.readline()

		user_client = Client(
			f'sessions/user_{__id}',
			session_string=session_string
		)
		await user_client.start()
		# await user_client.connect()

		d = await Users.get_user(message.from_user.id)
		sCode_hash = d['sCode_hash']
		phone = d['phone']

		req = await user_client.sign_in(phone, sCode_hash, message.text)

		await user_client.disconnect()
