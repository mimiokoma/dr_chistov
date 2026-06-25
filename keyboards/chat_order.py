from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def order_chat_keyboard(order_id: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Выполнено",
                    callback_data=f"done_{order_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data=f"cancel_{order_id}"
                )
            ]
        ]
    )