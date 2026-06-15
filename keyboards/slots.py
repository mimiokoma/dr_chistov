from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton



slots_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Добавить слоты",
                callback_data="add_slots"
            )
        ],
        [
            InlineKeyboardButton(
                text="➖ Удалить слоты",
                callback_data="delete_slots"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Все слоты",
                callback_data="all_slots"
            )
        ]
    ]
)

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


WORK_HOURS = [
    "09:00",
    "09:30",

    "10:00",
    "10:30",

    "11:00",
    "11:30",

    "12:00",
    "12:30",

    "13:00",
    "13:30",

    "14:00",
    "14:30",

    "15:00",
    "15:30",

    "16:00",
    "16:30",

    "17:00",
    "17:30",

    "18:00",
    "18:30",

    "19:00",
    "19:30",

    "20:00",
]


def build_time_keyboard(
        selected_times: list[str]
):

    keyboard = []

    row = []

    for index, time in enumerate(WORK_HOURS):

        mark = "✅" if time in selected_times else "☐"

        row.append(
            InlineKeyboardButton(
                text=f"{mark} {time}",
                callback_data=f"time_{time}"
            )
        )

        if len(row) == 3:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(
                text="💾 Сохранить",
                callback_data="save_slots"
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="add_slots"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )

def build_delete_dates_keyboard(dates):

    keyboard = []

    for (date,) in dates:

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=date,
                    callback_data=f"delete_date_{date}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="slots_menu"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )

def build_delete_slots_keyboard(
        slots,
        selected_ids
):

    keyboard = []

    row = []

    for slot_id, time in slots:

        mark = (
            "❌"
            if slot_id in selected_ids
            else "✅"
        )

        row.append(
            InlineKeyboardButton(
                text=f"{mark} {time}",
                callback_data=f"delslot_{slot_id}"
            )
        )

        if len(row) == 3:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(
                text="🗑 Удалить выбранные",
                callback_data="confirm_delete_slots"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )