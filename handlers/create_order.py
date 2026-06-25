import re

from aiogram import Router, F

from database.requests import (
    book_slot,
    unbook_slot
)

from keyboards.chat_order import (
    order_chat_keyboard
)

from database.requests import (
    add_completed_order
)

from config import WORK_CHAT_ID

from keyboards.order_dates import (
    build_dates_keyboard
)

from keyboards.sources import (
    sources_keyboard
)

from keyboards.order_times import (
    build_times_keyboard
)

from database.requests import (
    get_order_dates,
    get_order_times
)

from aiogram.types import Message
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext

from keyboards.services import (
    build_services_keyboard,
    SERVICES
)



from states.order_states import (
    CreateOrder
)

router = Router()




from keyboards.services import (
    build_services_keyboard,
    SERVICES
)

@router.message(
    F.text == "📋 Создать заявку"
)
async def create_order(
        message: Message,
        state: FSMContext
):

    await state.set_state(
        CreateOrder.services
    )

    await state.update_data(
        selected_services=[]
    )

    await message.answer(
        "Что чистить?",
        reply_markup=
        build_services_keyboard([])
    )

@router.callback_query(
    F.data.startswith("service_")
)
async def select_service(
        callback: CallbackQuery,
        state: FSMContext
):

    service_id = callback.data.replace(
        "service_",
        ""
    )

    data = await state.get_data()

    selected = data.get(
        "selected_services",
        []
    )

    if service_id in selected:
        selected.remove(service_id)
    else:
        selected.append(service_id)

    await state.update_data(
        selected_services=selected
    )

    await callback.message.edit_reply_markup(
        reply_markup=
        build_services_keyboard(
            selected
        )
    )

    await callback.answer()

@router.callback_query(
    F.data == "services_next"
)
async def services_next(
        callback: CallbackQuery,
        state: FSMContext
):

    data = await state.get_data()

    selected = data.get(
        "selected_services",
        []
    )

    if not selected:

        await callback.answer(
            "Выберите хотя бы одну услугу",
            show_alert=True
        )

        return

    first_service = selected[0]

    await state.update_data(
        quantity_index=0,
        quantities={}
    )

    await state.set_state(
        CreateOrder.quantity
    )

    await callback.message.edit_text(
        f"Количество:\n\n"
        f"{SERVICES[first_service]}"
    )

    await callback.answer()

@router.message(
    CreateOrder.quantity
)
async def input_quantity(
        message: Message,
        state: FSMContext
):

    if not message.text.isdigit():

        await message.answer(
            "Введите число"
        )
        return

    quantity = int(message.text)

    data = await state.get_data()

    selected = data[
        "selected_services"
    ]

    index = data[
        "quantity_index"
    ]

    quantities = data[
        "quantities"
    ]

    service_id = selected[index]

    quantities[service_id] = quantity

    index += 1

    if index >= len(selected):
        await state.update_data(
            quantities=quantities
        )

        dates = await get_order_dates()

        await state.set_state(
            CreateOrder.date
        )

        await message.answer(
            "Выберите дату",
            reply_markup=
            build_dates_keyboard(
                dates
            )
        )

        return

    await state.update_data(
        quantity_index=index,
        quantities=quantities
    )

    next_service = selected[index]

    await message.answer(
        f"Количество:\n\n"
        f"{SERVICES[next_service]}"
    )

@router.callback_query(
    F.data.startswith("order_date_")
)
async def choose_date(
        callback: CallbackQuery,
        state: FSMContext
):

    date = callback.data.replace(
        "order_date_",
        ""
    )

    await state.update_data(
        date=date
    )

    times = await get_order_times(
        date
    )

    await state.set_state(
        CreateOrder.time
    )

    await callback.message.edit_text(
        f"📅 {date}\n\n"
        f"Выберите время",
        reply_markup=
        build_times_keyboard(
            times
        )
    )

    await callback.answer()

@router.callback_query(
    F.data.startswith("order_time_")
)
async def choose_time(
        callback: CallbackQuery,
        state: FSMContext
):

    time = callback.data.replace(
        "order_time_",
        ""
    )

    await state.update_data(
        time=time
    )

    await state.set_state(
        CreateOrder.client_name
    )

    await callback.message.edit_text(
        "Введите имя клиента"
    )

    await callback.answer()

@router.message(
    CreateOrder.client_name
)
async def get_client_name(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        client_name=message.text
    )

    await state.set_state(
        CreateOrder.client_phone
    )

    await message.answer(
        "Введите телефон клиента"
    )

@router.message(
    CreateOrder.client_phone
)
async def get_phone(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        client_phone=message.text
    )

    await state.set_state(
        CreateOrder.address
    )

    await message.answer(
        "Введите адрес"
    )

@router.message(
    CreateOrder.address
)
async def get_address(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        address=message.text
    )

    await state.set_state(
        CreateOrder.source
    )

    await message.answer(
        "Источник заявки",
        reply_markup=sources_keyboard
    )

@router.callback_query(
    F.data.startswith("source_")
)
async def get_source(
        callback: CallbackQuery,
        state: FSMContext
):

    source_map = {
        "source_vk": "VK",
        "source_tg": "Telegram",
        "source_inst": "Instagram",
        "source_call": "Звонок",
        "source_site": "Сайт",
        "source_max": "MAX"
    }

    source = source_map[
        callback.data
    ]

    await state.update_data(
        source=source
    )

    await state.set_state(
        CreateOrder.price
    )

    await callback.message.edit_text(
        "Введите стоимость"
    )

    await callback.answer()

@router.message(
    CreateOrder.price
)
async def get_price(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        price=message.text
    )

    await state.set_state(
        CreateOrder.comment
    )

    await message.answer(
        "Дополнительная информация"
    )

from keyboards.order_confirm import (
    skip_photo_keyboard,
    confirm_keyboard
)

@router.message(
    CreateOrder.comment
)
async def get_comment(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        comment=message.text
    )

    await state.set_state(
        CreateOrder.photo
    )

    await message.answer(
        "Прикрепите фото",
        reply_markup=skip_photo_keyboard
    )

def build_order_text(data):

    services_text = ""

    for service_id, qty in data[
        "quantities"
    ].items():

        service_names = {
            "sofa": "🛋 Диван",
            "mattress": "🛏 Матрас",
            "armchair": "💺 Кресло",
            "chairs": "🪑 Стулья"
        }

        services_text += (
            f"{service_names[service_id]} × {qty}\n"
        )

    return (
        "📌 Химчистка\n\n"

        f"{services_text}\n"

        f"📅 {data['date']}\n"
        f"⏰ {data['time']}\n\n"

        f"👤 Клиент\n"
        f"{data['client_name']}\n"
        f"{data['client_phone']}\n\n"

        f"📍 {data['address']}\n\n"

        f"🔗 Источник: {data['source']}\n\n"

        f"💰 {data['price']} рублей\n\n"

        f"🏷️ {data['comment']}"
    )

@router.message(
    CreateOrder.photo,
    F.photo
)
async def get_photo(
        message: Message,
        state: FSMContext
):

    photo_id = message.photo[-1].file_id

    await state.update_data(
        photo=photo_id
    )

    data = await state.get_data()

    await state.set_state(
        CreateOrder.confirm
    )

    await message.answer(
        build_order_text(data),
        reply_markup=confirm_keyboard
    )

@router.callback_query(
    F.data == "skip_photo"
)
async def skip_photo(
        callback: CallbackQuery,
        state: FSMContext
):

    await state.update_data(
        photo=None
    )

    data = await state.get_data()

    await state.set_state(
        CreateOrder.confirm
    )

    await callback.message.edit_text(
        build_order_text(data),
        reply_markup=confirm_keyboard
    )

    await callback.answer()

@router.callback_query(
    F.data == "confirm_order"
)
async def confirm_order(
        callback: CallbackQuery,
        state: FSMContext
):

    data = await state.get_data()

    text = build_order_text(data)

    services = []

    if data.get("photo"):

        await callback.bot.send_photo(
            chat_id=WORK_CHAT_ID,
            photo=data["photo"],
            caption=text,
            reply_markup=order_chat_keyboard()
        )

    else:

        await callback.bot.send_message(
            chat_id=WORK_CHAT_ID,
            text=text,
            reply_markup=order_chat_keyboard()
        )



    await book_slot(
        data["date"],
        data["time"]
    )

    await state.clear()

    await callback.message.edit_text(
        "✅ Заявка отправлена"
    )

    await callback.answer()

@router.callback_query(
    F.data.startswith("done_")
)
async def done_order(
        callback: CallbackQuery
):
    order_id = int(
        callback.data.replace(
            "done_",
            ""
        )
    )
    text = (
        callback.message.caption
        or
        callback.message.text
    )

    amount = 0

    for line in text.split("\n"):

        if "💰" in line:

            numbers = re.findall(r"\d+", line)

            if numbers:
                amount = sum(map(int, numbers))

            break

    await add_completed_order(
        amount
    )

    await callback.message.edit_reply_markup(
        reply_markup=None
    )

    if callback.message.photo:

        await callback.message.edit_caption(
            caption=
            text +
            "\n\n━━━━━━━━━━━━\n"
            "✅ Выполнено"
        )

    else:

        await callback.message.edit_text(
            text +
            "\n\n━━━━━━━━━━━━\n"
            "✅ Выполнено"
        )

    await callback.answer(
        "Заказ выполнен"
    )

@router.callback_query(
    F.data.in_({"cancel_order"}) |
    F.data.startswith("cancel_")
)
async def cancel_order(
        callback: CallbackQuery
):
    text = callback.message.caption or callback.message.text

    date = None
    time = None

    for line in text.split("\n"):
        if line.startswith("📅"):
            date = line.replace("📅", "").strip()

        if line.startswith("⏰"):
            time = line.replace("⏰", "").strip()

    if date and time:
        await unbook_slot(date, time)

    await callback.message.edit_reply_markup(
        reply_markup=None
    )

    if callback.message.photo:

        await callback.message.edit_caption(
            caption=
            text +
            "\n\n━━━━━━━━━━━━\n"
            "❌ Отменено"
        )

    else:

        await callback.message.edit_text(
            text +
            "\n\n━━━━━━━━━━━━\n"
            "❌ Отменено"
        )

    await callback.answer(
        "Заказ отменён"
    )