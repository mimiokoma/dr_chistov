from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def build_times_keyboard(
    times,
    prefix="order_time"
):

    keyboard = []

    row = []

    for (time,) in times:

        row.append(
            InlineKeyboardButton(
                text=time,
                callback_data=f"{prefix}_{time}"
            )
        )

        if len(row) == 3:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )