import asyncio

from handlers.profit import (
    router as profit_router
)


from aiogram import Bot, Dispatcher

from handlers.create_order import (
    router as create_order_router
)

from config import BOT_TOKEN
from database.database import init_db

from handlers.start import router as start_router

from handlers.slots import router as slots_router
from handlers.free_dates import router as free_dates_router

async def main():

    await init_db()

    bot = Bot(BOT_TOKEN)

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(
        create_order_router
    )
    dp.include_router(slots_router)
    dp.include_router(free_dates_router)
    dp.include_router(
        profit_router
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())