from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def build_dates_keyboard(dates):

    keyboard = []

    for (date,) in dates:

        short_date = ".".join(
            date.split(".")[:2]
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"📅 {short_date}",
                    callback_data=f"order_date_{date}"
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )