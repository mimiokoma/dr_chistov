from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📋 Создать заявку")
        ],
        [
            KeyboardButton(text="📅 Управление датами")
        ],
        [
            KeyboardButton(text="📆 Свободные даты")
        ],
        [
            KeyboardButton(text="📈 Прибыль")
        ],
    ],
    resize_keyboard=True
)
