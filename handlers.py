from pyrogram import Client
from pyrogram import filters, types
from pyrogram.handlers import MessageHandler

from db_controllers.user_db import Users
from filters import Filters
from mailing import Mailing

from loguru import logger
import hashlib


class BaseHandler:
	def __init__(self, bot):
		bot.add_handler(
			MessageHandler(
				BaseHandler.start,
				filters=filters.command('start')
			)
		)
		logger.info('\t-- BaseHandler initialized --')

	@staticmethod
	async def start(client: Client, message: types.Message):
		if not await Users.user_exist(message.from_user.id):
			await Users.user_add(message.from_user.id)

			text = \
				f'Здравствуй, {message.from_user.first_name}, для Рассылки мне необходим ваш <b>api_id</b> и ' \
				f'<b>api_hash</b>. \nНапишите /help_reg для получения инструкциии.'

			await client.send_message(message.from_user.id, text=text)


class RegistrationHandler:
	def __init__(self, bot):
		bot.add_handler(
			MessageHandler(
				RegistrationHandler._help,
				filters=filters.command('help_reg')
			)
		)
		# bot.add_handler(
		# 	MessageHandler(
		# 		RegistrationHandler.reg,
		# 		filters=filters.command('reg')
		# 	)
		# )
		# bot.add_handler(
		# 	MessageHandler(
		# 		RegistrationHandler.code,
		# 		filters=Filters.reg_mode() & Filters.sCode_hash_is_not_None()
		# 	)
		# )

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

	# @staticmethod
	# async def _help_reg(client: Client, message: types.Message):
	# 	text = f''''''
	# 	await client.send_message(message.from_user.id, text=text)

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


class SendHandler:
	def __init__(self, bot):
		bot.add_handler(
			MessageHandler(
				SendHandler.help_send_,
				filters=filters.command('help_send')
			)
		)

		bot.add_handler(
			MessageHandler(
				SendHandler.send,
				filters=filters.command('send')
			)
		)

		SendHandler.RecordingMessages(bot)

		bot.add_handler(
			MessageHandler(
				SendHandler.interval,
				filters=filters.command('interval') & Filters.send_mode()
			)
		)
		bot.add_handler(
			MessageHandler(
				SendHandler.recipients,
				filters=filters.command('recipients') & Filters.send_mode()
			)
		)
		bot.add_handler(
			MessageHandler(
				SendHandler.file_d,
				filters=filters.document & Filters.send_mode() & Filters.waiting_for_a_file() & Filters.doc_type(
					'text/plain')
			)
		)
		bot.add_handler(
			MessageHandler(
				SendHandler.test,
				filters=filters.command('test') & Filters.send_mode()
			)
		)
		bot.add_handler(
			MessageHandler(
				SendHandler.go,
				filters=filters.command('go') & Filters.send_mode()
			)
		)
		bot.add_handler(
			MessageHandler(
				SendHandler.stop,
				filters=filters.command('stop') & Filters.send_mode()
			)
		)
		logger.info('\t-- SendHandler initialized --')

	@staticmethod
	async def help_send_(client: Client, message: types.Message):
		...

	@staticmethod
	async def send(client: Client, message: types.Message):
		await Users.user_update_send_mode(message.from_user.id, True)

	class RecordingMessages:
		def __init__(self, bot):
			bot.add_handler(
				MessageHandler(
					SendHandler.RecordingMessages.begin,
					filters=filters.command('begin') & Filters.send_mode()
				)
			)
			bot.add_handler(
				MessageHandler(
					SendHandler.RecordingMessages.end,
					filters=filters.command('end') & Filters.send_mode() & Filters.read_mode()
				)
			)
			bot.add_handler(
				MessageHandler(
					SendHandler.RecordingMessages.rw,
					filters=Filters.send_mode() & Filters.read_mode()
				)
			)

		# @client.on_message(filters.command('begin') & Filters.send_mode())
		@staticmethod
		async def begin(client: Client, message: types.Message):
			await Users.user_update_messages(message.from_user.id, [])
			await Users.user_update_read_mode(message.from_user.id, True)

		# @client.on_message(filters.command('end') & Filters.send_mode() & Filters.read_mode())
		@staticmethod
		async def end(client: Client, message: types.Message):
			await Users.user_update_read_mode(message.from_user.id, False)

		# @client.on_message(Filters.send_mode() & Filters.read_mode())
		@staticmethod
		async def rw(client: Client, message: types.Message):
			_data = await Users.get_user(message.from_user.id)
			await Users.user_update_messages(message.from_user.id, _data['messages'] + [message.id])

	@staticmethod
	async def interval(client: Client, message: types.Message):
		await Users.user_update_interval(message.from_user.id, list(map(int, message.text.split()[1:])))

	@staticmethod
	async def recipients(client: Client, message: types.Message):
		await Users.user_update_recipients(message.from_user.id, message.text.split()[1])
		if message.text.split()[1] == 'file':
			await Users.user_update_waiting_for_a_file(message.from_user.id, True)

	@staticmethod
	async def file_d(client: Client, message: types.Message):
		__id = hashlib.sha256(str(message.from_user.id).encode()).hexdigest()
		await client.download_media(message, f'data/temp/{__id}.txt')
		await Users.user_update_waiting_for_a_file(message.from_user.id, False)

	@staticmethod
	async def test(client: Client, message: types.Message):
		user_data = await Users.get_user(message.from_user.id)
		messages_id = user_data['messages']
		for _message_id in messages_id:
			await client.copy_message(
				chat_id=message.chat.id,
				from_chat_id=message.chat.id,
				message_id=_message_id
			)

	@staticmethod
	async def go(client: Client, message: types.Message):
		d = await Users.get_user(message.from_user.id)
		if d['recipients'] == 'all':
			await Mailing.mailing_to_everyone(client, message)
		elif d['recipients'] == 'file':
			await Mailing.mailing_by_file(client, message)

	@staticmethod
	async def stop(client: Client, message: types.Message):
		await Users.user_update_send_mode(message.from_user.id, False)
		
		# вернуть файл с не оповещенными пользователями
