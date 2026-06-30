from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


SERVICES = {
    "sofa": "🛋 Диван",
    "mattress": "🛏 Матрас",
    "armchair": "💺 Кресло",
    "chairs": "🪑 Стулья",
    "kover": "📃 Ковёр/ковролин"
}


def build_services_keyboard(
        selected_services: list[str]
):

    keyboard = []

    for service_id, title in SERVICES.items():

        mark = (
            "✅"
            if service_id in selected_services
            else "☐"
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{mark} {title}",
                    callback_data=
                    f"service_{service_id}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="➡️ Далее",
                callback_data="services_next"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )