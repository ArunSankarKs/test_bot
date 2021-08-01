# --------------------------------------------- #
# Plugin Name           : TelegramAirdropBot    #
# Author Name           : fabston               #
# File Name             : main.py               #
# --------------------------------------------- #
import datetime
import ssl
from io import BytesIO
from random import randint
from time import gmtime, strftime

import eth_utils
import pymysql
import telebot
from aiohttp import web
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import config

WEBHOOK_HOST = config.host
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port needs to be 'open')
WEBHOOK_LISTEN = "0.0.0.0"  # In some VPS you may need to put here the IP addr.

WEBHOOK_SSL_CERT = "./webhook_cert.pem"  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = "./webhook_pkey.pem"  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(config.api_token)

bot = telebot.TeleBot(config.api_token)

app = web.Application()


@bot.message_handler(commands=["/start"])
def price(message):
    bot.send_message(message, text="Hello there")
    print(datetime.datetime.now)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(
    url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, "r")
)

# Build ssl context
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

# Start aiohttp server
web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=context,
)
