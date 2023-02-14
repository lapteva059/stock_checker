from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url='postgres://admin:admin@localhost:5432/tammytanuka',
        modules={'models': ['models']}
    )

# async def init_test_db():
#     await Tortoise.init(
#
#         db_url='postgres://admin:admin@localhost:5432/tammytanukatest',
#         modules={'models': ['models']}
#     )