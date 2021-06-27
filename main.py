import logging
import os

from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

import train
from chat import botchat
from dotenv import load_dotenv
load_dotenv()
updater = Updater(token=os.getenv('PERMISO'), use_context=True)
dispatcher = updater.dispatcher
logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


def start(update, context):
    user = update.message.from_user
    logger.info("%s %s %s %s %s", datetime.now(), user.id, user.first_name, user.last_name, user.username)
    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.MARKDOWN,
                             text="Puedes preguntarme sobre la *Metodología para la Gestión de la Seguridad Informática en CUBA*"
                                  ". También puedes usar los comandos /link y /send para referirte donde encontrar el contenido")


def link(update, context):
    user = update.message.from_user
    logger.info("%s %s %s %s %s", datetime.now(), user.id, user.first_name, user.last_name, user.username)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="https://telegra.ph/Gaceta-Oficial-No-45-Ordinaria-de-2019-06-26?r=83665923",
                             disable_web_page_preview=False)


def send(update, context):
    user = update.message.from_user
    logger.info("%s %s %s %s %s", datetime.now(), user.id, user.first_name, user.last_name, user.username)
    filename = 'doc/GOC-45-Leyes cubanas-4-7-19.pdf'
    context.bot.send_document(chat_id=update.effective_chat.id, document=open(filename, 'rb'),
                              filename="GOC-45-Leyes cubanas-4-7-19",
                              caption='En el mismo puede buscar la Resolución 129')


def etrain(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text=train.complete_train())


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Lo siento, este comando no lo entiendo.")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=botchat(update.message.text))


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

link_handler = CommandHandler('link', link)
dispatcher.add_handler(link_handler)

send_handler = CommandHandler('send', send)
dispatcher.add_handler(send_handler)

send_handler = CommandHandler('train', etrain)
dispatcher.add_handler(send_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
