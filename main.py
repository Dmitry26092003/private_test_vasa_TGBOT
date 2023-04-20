from settings import config

from pyrogram import Client

from handlers import BaseHandler, SendHandler
from reg_user import RegistrationHandler

from loguru import logger


bot = Client(
	"private_test_vasa_bot",
	api_id=config['API_ID'], api_hash=config['API_HASH'],
	bot_token=config['TOKEN']
)

BaseHandler(bot)
RegistrationHandler(bot)
SendHandler(bot)


if __name__ == '__main__':
	logger.info('\t-- Bot Started --')
	bot.run()
