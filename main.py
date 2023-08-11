# блок импортов
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    ConversationHandler
)
from telegram.ext.filters import Filters
from config import TOKEN
from functions import *


# сам бот и его зам
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

# хэндлеры
game_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],  # точка входа
    states={
        GAME: [MessageHandler(Filters.text & ~Filters.command, game)]
    },  # шаги разговора
    fallbacks=[CommandHandler("cancel", cancel)]  # точка выхода
)
# добавляем хэндлеры диспетчеру
dispatcher.add_handler(game_handler)

print("Server started")
updater.start_polling()
updater.idle()
