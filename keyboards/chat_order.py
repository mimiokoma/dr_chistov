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
                    text="✏️ Изменить",
                    callback_data=f"edit_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📅 Перенести",
                    callback_data=f"move_{order_id}"
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