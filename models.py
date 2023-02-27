from tortoise.models import Model
from tortoise import fields
from tg_bot.tg_bot_loader import bot
from tg_bot.tg_bot import MESSAGES


class Stock(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(unique=True, max_length=200)
    in_stock = fields.BooleanField(default=False)  # 0 if out of stock, 1 if in stock
    url = fields.TextField(null=True)
    created_date = fields.DatetimeField(auto_now_add=True, null=False)
    updated_date = fields.DatetimeField(auto_now=True, null=False)
    new_product = fields.BooleanField(default=False)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def __eq__(self, other):
        return self.title == other.title # && self.url == other.url

    def __hash__(self):
        return hash(self.title)

    @property
    def new_stock_message(self):
        return MESSAGES['new_stock_message'].format(title=self.title, url=self.url)

    async def notify_subscribers(self, message):
        try:
            subscribers = [chats_id.chat_id
                           for chats_id in await ChatId.all()]
        except Exception:
            subscribers = []
        if subscribers:
            for subscriber in subscribers:
                await bot.send_message(chat_id=subscriber, text=message)


class ChatId(Model):
    chat_id = fields.CharField(max_length=50, null=True, blank=True, unique=True)



