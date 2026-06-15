import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def build_calendar(year: int, month: int):

    kb = []

    month_name = datetime(year, month, 1).strftime("%B %Y")

    kb.append(
        [
            InlineKeyboardButton(
                text=f"📅 {month_name}",
                callback_data="ignore"
            )
        ]
    )

    kb.append(
        [
            InlineKeyboardButton(text="Пн", callback_data="ignore"),
            InlineKeyboardButton(text="Вт", callback_data="ignore"),
            InlineKeyboardButton(text="Ср", callback_data="ignore"),
            InlineKeyboardButton(text="Чт", callback_data="ignore"),
            InlineKeyboardButton(text="Пт", callback_data="ignore"),
            InlineKeyboardButton(text="Сб", callback_data="ignore"),
            InlineKeyboardButton(text="Вс", callback_data="ignore"),
        ]
    )

    cal = calendar.monthcalendar(year, month)

    today = datetime.now().date()

    for week in cal:

        row = []

        for day in week:

            if day == 0:

                row.append(
                    InlineKeyboardButton(
                        text=" ",
                        callback_data="ignore"
                    )
                )

            else:

                current_date = datetime(
                    year,
                    month,
                    day
                ).date()

                if current_date < today:

                    row.append(
                        InlineKeyboardButton(
                            text="➖",
                            callback_data="ignore"
                        )
                    )

                else:

                    row.append(
                        InlineKeyboardButton(
                            text=str(day),
                            callback_data=f"date_{day}_{month}_{year}"
                        )
                    )

        kb.append(row)

    prev_month = month - 1
    prev_year = year

    if prev_month < 1:
        prev_month = 12
        prev_year -= 1

    next_month = month + 1
    next_year = year

    if next_month > 12:
        next_month = 1
        next_year += 1

    kb.append(
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"month_{prev_month}_{prev_year}"
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"month_{next_month}_{next_year}"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=kb
    )