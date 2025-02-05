import os
import logging
# from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
)
from text_messege import ABOUT_MES, AUTHOR
from genegate_seleg import genegate, get_balance

# load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


"""Начальный экран."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    replay_markup = ReplyKeyboardMarkup(
        [['Начать', 'О боте'], ['Автор']],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Привет, я бот, который поможет вам составить поздравление.',
        reply_markup=replay_markup
    )


"""Выбор параметров поздравления."""


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    replay_markup = ReplyKeyboardMarkup(
        [['Вернуться в начало']],
        resize_keyboard=True
    )
    key = update.message.from_user.id
    if update.message.text == 'Начать':
        context.user_data[key] = [update.message.text]
    else:
        context.user_data[key].append(update.message.text)
    out = context.user_data.get(key, 'Not found')
    if out[-1] == 'Начать':
        text = 'Напишите имя или имена, кого вы хотите поздравить.'
    elif out[-2] == 'Начать':
        text = 'Напишите повод с которым вы хотите поздравить.'
    elif out[-3] == 'Начать':
        text = f'Напишите 2-3 прилагательных которые описывают {out[-2]}.'
    else:
        text = genegate(out[-3], out[-2], out[-1])
        context.user_data[key] = []
        replay_markup = ReplyKeyboardMarkup(
            [['Начать', 'О боте'], ['Автор']],
            resize_keyboard=True
        )
        user = update.effective_chat.username
        await context.bot.send_message(
            chat_id=int(os.getenv('CREATOR')),
            text = user + ' - сгенерировал что то.',
            reply_markup=None
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=replay_markup
    )


"""Информация о боте"""


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    replay_markup = ReplyKeyboardMarkup(
        [['Начать', 'О боте'], ['Автор']],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ABOUT_MES + str(get_balance())
    )

"""При низком балансе"""


async def low_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    replay_markup = ReplyKeyboardMarkup(
        [['О боте', 'Автор']],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Баланс токенов слимшком низкий что бы что то сгенерировать!'
    )


"""Вывод команды о ошибке."""


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    replay_markup = ReplyKeyboardMarkup(
        [['Начать', 'О боте'], ['Автор']],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Команда не распознана, воспользуйтесь кнопками',
        reply_markup=replay_markup
    )

"""Функция обработки сообщений."""


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last = context.user_data.get(update.message.from_user.id, 'Not found')
    text = update.message.text
    key = update.message.from_user.id
    data = context.user_data.get(key, 'Not found')
    logging.info(text)
    if text == 'Вернуться в начало':
        context.user_data[key] = []
        await start(update, context)
    elif text == 'О боте':
        await about(update, context)
    elif text == 'Автор':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=AUTHOR
        )
    elif get_balance() < 500:
        await low_balance(update, context)
    elif text == 'Начать' or data[0] == 'Начать':
        await name(update, context)
    else:
        await unknown(update, context)

if __name__ == '__main__':
    application = ApplicationBuilder().token(
        os.getenv('TELEGRAM_TOKEN')
    ).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    message_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    application.run_polling()
