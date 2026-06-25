from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def order_chat_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Выполнено",
                    callback_data=f"done_"
                )
            ],

            [
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data=f"cancel_"
                )
            ]
        ]
    )