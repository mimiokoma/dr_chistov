from aiogram import Router
from aiogram.types import Message

from database.requests import get_free_slots


router = Router()


@router.message(
    lambda m: m.text == "📆 Свободные даты"
)
async def free_dates(message: Message):

    slots = await get_free_slots()

    if not slots:

        await message.answer(
            "Свободных слотов нет"
        )

        return

    grouped = {}

    for date, time in slots:

        if date not in grouped:
            grouped[date] = []

        grouped[date].append(time)

    text = "📆 Свободные слоты\n\n"

    for date in grouped:

        grouped[date].sort()
        short_date = ".".join(date.split(".")[:2])

        text += (
            f"{short_date} - "
            f"{', '.join(grouped[date])}\n\n"
        )

    await message.answer(text)