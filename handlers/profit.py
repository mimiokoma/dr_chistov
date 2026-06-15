from aiogram import Router
from aiogram import F

from aiogram.types import Message

from database.requests import (
    get_month_profit
)

router = Router()


@router.message(
    F.text == "📈 Прибыль"
)
async def show_profit(
        message: Message
):

    profit = await get_month_profit()

    await message.answer(
        f"📈 Прибыль за месяц\n\n"
        f"{profit:,} ₽".replace(
            ",",
            " "
        )
    )