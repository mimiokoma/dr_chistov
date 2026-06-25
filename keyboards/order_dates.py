from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def build_dates_keyboard(
    dates,
    prefix="order_date"
):

    keyboard = []

    for (date,) in dates:

        short = ".".join(
            date.split(".")[:2]
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"📅 {short}",
                    callback_data=f"{prefix}_{date}"
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )