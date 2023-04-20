from pyrogram import filters, types
from db_controllers.user_db import Users


class Filters:
	@staticmethod
	def read_mode() -> filters:
		async def _filter(_, __, message: types.Message):
			d = await Users.get_user(message.from_user.id)
			return d['read_mode']
		return filters.create(_filter)

	@staticmethod
	def send_mode() -> filters:
		async def _filter(_, __, message: types.Message):
			d = await Users.get_user(message.from_user.id)
			return d['send_mode']

		return filters.create(_filter)

	@staticmethod
	def waiting_for_a_file() -> filters:
		async def _filter(_, __, message: types.Message):
			d = await Users.get_user(message.from_user.id)
			return d['waiting_for_a_file']

		return filters.create(_filter)

	@staticmethod
	def user_new() -> filters:
		async def _filter(_, __, message: types.Message):
			return not await Users.user_exist(message.from_user.id)

		return filters.create(_filter)

	@staticmethod
	def doc_type(_type: str) -> filters:
		async def _filter(_, __, message: types.Message):
			return message.document.mime_type == _type

		return filters.create(_filter)

	@staticmethod
	def reg_mode() -> filters:
		async def _filter(_, __, message: types.Message):
			d = await Users.get_user(message.from_user.id)
			return d['reg_mode']

		return filters.create(_filter)

	@staticmethod
	def sCode_hash_is_not_None() -> filters:
		async def _filter(_, __, message: types.Message):
			d = await Users.get_user(message.from_user.id)
			return not (d['sCode_hash'] is None)

		return filters.create(_filter)
