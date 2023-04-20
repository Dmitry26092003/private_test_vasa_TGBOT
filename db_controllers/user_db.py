from motor import motor_asyncio
from settings import config
import hashlib

from loguru import logger


class Users:
	@staticmethod
	def connect_to_db() -> (
			motor_asyncio.AsyncIOMotorClient,
			motor_asyncio.AsyncIOMotorDatabase,
			motor_asyncio.AsyncIOMotorCollection
	):
		client: motor_asyncio.AsyncIOMotorClient = motor_asyncio.AsyncIOMotorClient(config['MONGODB'])
		db = client.vasa_tg
		collection = db.users
		return client, db, collection

	@staticmethod
	async def user_exist(__id):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()
		rez = await collection.count_documents({'_id': __id})

		return bool(rez)

	@staticmethod
	async def user_add(__id):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()
		_data = {
			'_id': __id,  # hash
			'registered': False,

			'reg_mode': False,
			'send_mode': False,
			'read_mode': False,
			'waiting_for_a_file': False,

			'API_ID': None,  # str
			'API_HASH': None,  # str
			'sCode_hash': None,  # str
			'phone': None,  # str: '+7XXXXXXXXXX'

			'messages': [],
			'interval': [],  # [int] | [int, int]
			'recipients': None,  # 'all' | 'file'
		}
		rez = await collection.insert_one(_data)
		logger.info(f'DB | {rez}')

	@staticmethod
	async def user_rem(__id):  # Удалить пользователя
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		rez = await collection.delete_one({'_id': __id})
		logger.info(f'DB | {rez}')

	# update registered
	@staticmethod
	async def user_update_registered(__id, registered):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		_data = {
			'registered': registered
		}

		rez = await collection.update_one({'_id': __id}, {'$set': _data})
		logger.info(f'DB | {rez}')

	# update modes
	@staticmethod
	async def user_update_reg_mode(__id, reg_mode):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		_data = {
			'reg_mode': reg_mode
		}

		rez = await collection.update_one({'_id': __id}, {'$set': _data})
		logger.info(f'DB | {rez}')

	@staticmethod
	async def user_update_send_mode(__id, send_mode):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		_data = {
			'send_mode': send_mode
		}

		rez = await collection.update_one({'_id': __id}, {'$set': _data})
		logger.info(f'DB | {rez}')

	@staticmethod
	async def user_update_read_mode(__id, read_mode):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		_data = {
			'read_mode': read_mode
		}

		rez = await collection.update_one({'_id': __id}, {'$set': _data})
		logger.info(f'DB | {rez}')

	@staticmethod
	async def user_update_waiting_for_a_file(__id, waiting_for_a_file):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		_data = {
			'waiting_for_a_file': waiting_for_a_file
		}

		rez = await collection.update_one({'_id': __id}, {'$set': _data})
		logger.info(f'DB | {rez}')

	# update user data
	@staticmethod
	async def user_update_api_id(__id, api_id):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		_data = {
			'API_ID': api_id
		}

		rez = await collection.update_one({'_id': __id}, {'$set': _data})
		logger.info(f'DB | {rez}')

	@staticmethod
	async def user_update_api_hash(__id, api_hash):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		_data = {
			'API_HASH': api_hash
		}

		rez = await collection.update_one({'_id': __id}, {'$set': _data})
		logger.info(f'DB | {rez}')

	@staticmethod
	async def user_update_sCode_hash(__id, sCode_hash):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		_data = {
			'sCode_hash': sCode_hash
		}

		rez = await collection.update_one({'_id': __id}, {'$set': _data})
		logger.info(f'DB | {rez}')

	@staticmethod
	async def user_update_phone(__id, phone):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		_data = {
			'phone': phone
		}

		rez = await collection.update_one({'_id': __id}, {'$set': _data})
		logger.info(f'DB | {rez}')

	#
	@staticmethod
	async def user_update_messages(__id, messages):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		_data = {
			'messages': messages
		}

		rez = await collection.update_one({'_id': __id}, {'$set': _data})
		logger.info(f'DB | {rez}')

	@staticmethod
	async def user_update_recipients(__id, recipients):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		_data = {
			'recipients': recipients
		}

		rez = await collection.update_one({'_id': __id}, {'$set': _data})
		logger.info(f'DB | {rez}')

	@staticmethod
	async def user_update_interval(__id, interval):
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		_data = {
			'interval': interval
		}

		rez = await collection.update_one({'_id': __id}, {'$set': _data})
		logger.info(f'DB | {rez}')

	#
	@staticmethod
	async def get_user(__id) -> dict:
		__id = hashlib.sha256(str(__id).encode()).hexdigest()

		client, db, collection = Users.connect_to_db()

		rez = await collection.find_one({'_id': __id})

		return rez
