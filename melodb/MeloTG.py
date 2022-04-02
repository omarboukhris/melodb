
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from melodb.loggers import MongoLogger

class MeloTelegramHandler:
	# TODO : add commands

	@staticmethod
	def start(update: Update, context: CallbackContext):
		ss = "Welcome to MeloTG:\n\n"
		ss += "/start /help /menu : Display this message\n"
		update.message.reply_text(ss)

	@staticmethod
	def test_args(update: Update, context: CallbackContext):
		print(context.args)

	@staticmethod
	def get_logs(update: Update, context: CallbackContext):
		try:
			nb_logs = int(context.args[0]) if len(context.args) == 1 else 10
		except Exception as e:
			print(f"An unexpected exception occured : {e}")
			nb_logs = 10

		mongo_loggger = MongoLogger("mglogger-test")

		for log in mongo_loggger.get_last_logs(nb_logs):
			ss = f"{log['type']} [{log['date']}] [{log['component']}] : {log['message']}"
			update.message.reply_text(ss)

	@staticmethod
	def unknown(update: Update, context: CallbackContext):
		pass


if __name__ == "__main__":
	with open("melo-tg.tok") as fs:
		tg_token = fs.readline()
		updater = Updater(tg_token, use_context=True)

	updater.dispatcher.add_handler(CommandHandler('start', MeloTelegramHandler.start))
	updater.dispatcher.add_handler(CommandHandler('menu', MeloTelegramHandler.start))
	updater.dispatcher.add_handler(CommandHandler('help', MeloTelegramHandler.start))
	updater.dispatcher.add_handler(CommandHandler('logs', MeloTelegramHandler.get_logs, pass_args=True))
	updater.dispatcher.add_handler(MessageHandler(Filters.text, MeloTelegramHandler.unknown))
	updater.dispatcher.add_handler(MessageHandler(Filters.command, MeloTelegramHandler.unknown))

	updater.start_polling()
