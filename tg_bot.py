import logging

from aiogram import Bot, Dispatcher, executor, types
from settings import API_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

start_message = 'Привет! Я сообщу, когда что-то появится в наличии'
new_in_stock = '{title} в наличии! {url}'

MESSAGES = {
    'start': start_message,
    'new_in_stock_message': new_in_stock,
    }

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(MESSAGES['start'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)