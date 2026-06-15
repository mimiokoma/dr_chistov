from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)




skip_photo_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Пропустить",
                callback_data="skip_photo"
            )
        ]
    ]
)


confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Отправить",
                callback_data="confirm_order"
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