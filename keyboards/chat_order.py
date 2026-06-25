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
                    callback_data="done_order"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data="cancel_order"
                )
            ]
        ]
    )