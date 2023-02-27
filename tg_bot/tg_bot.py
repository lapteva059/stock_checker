import logging

from aiogram import executor, types
from asyncpg.exceptions import UniqueViolationError

from .tg_bot_loader import dp
import models

# Configure logging
logging.basicConfig(level=logging.INFO)

start_message = 'Привет! Я сообщу, когда что-то появится в наличии'
new_stock_message = '{title} в наличии!' \
                    ' {url}'

MESSAGES = {
    'start': start_message,
    'new_stock_message': new_stock_message,
    }


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat = models.ChatId(
        chat_id=message.chat.id,
        username=message.chat.username)
    try:
        await chat.save()
    except UniqueViolationError:
        pass
    await message.reply(MESSAGES['start'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
