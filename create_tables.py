from tortoise import Tortoise, run_async


async def init():
    await Tortoise.init(
        db_url='postgres://admin:admin@localhost:5432/tammytanuka',
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas(safe=False)

# run_async is a helper function to run simple async Tortoise scripts.
if __name__ == "__main__":
    run_async(init())
