from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def build_times_keyboard(times):

    keyboard = []

    row = []

    for (time,) in times:

        row.append(
            InlineKeyboardButton(
                text=time,
                callback_data=f"order_time_{time}"
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