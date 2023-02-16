from tortoise.models import Model
from tortoise import fields
from tg_bot_loader import bot
from tg_bot import new_stock_message

class Stock(Model):
    id = fields.IntField(pk=True)
    title = fields.TextField()
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

    async def notify(self, message):
        await bot.send_message(text=message)

