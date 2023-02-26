import logging

from aiogram import Bot, Dispatcher, executor, types
from settings import API_TOKEN

from models import ChatId

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

start_message = 'Привет! Я сообщу, когда что-то появится в наличии'
new_stock_message = '{title} в наличии! {url}'

MESSAGES = {
    'start': start_message,
    'new_stock_message': new_stock_message,
    }

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(MESSAGES['start'])
    chat_id = ChatId(chat_id=message.chat.id)
    await chat_id.save()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
