from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext

from states.order_states import EditOrderState

from database.requests import (
    get_order,
    update_order_field
)

from database.requests import (
    move_order,
    get_order_dates,
    get_order_times
)

from keyboards.order_dates import (
    build_dates_keyboard
)

from keyboards.order_times import (
    build_times_keyboard
)

from aiogram import Bot

router = Router()

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from keyboards.services import SERVICES

from keyboards.chat_order import order_chat_keyboard

def build_order_text_from_db(order):

    services = ""

    if order["service"]:

        for item in order["service"].split(";"):

            service_id, qty = item.split(":")

            services += (
                f"{SERVICES[service_id]} × {qty}\n"
            )

    return (
        "📌 Химчистка\n\n"

        f"{services}\n"

        f"📅 {order['date']}\n"
        f"⏰ {order['time']}\n\n"

        f"👤 Клиент\n"
        f"{order['client_name']}\n"
        f"{order['client_phone']}\n\n"

        f"📍 {order['address']}\n\n"

        f"🔗 Источник: {order['source']}\n\n"

        f"💰 {order['price']} рублей\n\n"

        f"🏷️ {order['comment']}"
    )

def edit_keyboard(order_id: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="💰 Стоимость",
                    callback_data=f"edit_price_{order_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="👤 Клиент",
                    callback_data=f"edit_client_{order_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="☎ Телефон",
                    callback_data=f"edit_phone_{order_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📍 Адрес",
                    callback_data=f"edit_address_{order_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📝 Комментарий",
                    callback_data=f"edit_comment_{order_id}"
                )
            ]
        ]
    )

@router.callback_query(
    F.data.startswith("edit_")
)
async def edit_order(
    callback: CallbackQuery
):

    if callback.data.startswith("edit_price_"):
        return

    if callback.data.startswith("edit_phone_"):
        return

    if callback.data.startswith("edit_address_"):
        return

    if callback.data.startswith("edit_comment_"):
        return

    if callback.data.startswith("edit_client_"):
        return

    order_id = int(
        callback.data.replace(
            "edit_",
            ""
        )
    )

    order = await get_order(order_id)

    if not order:

        await callback.answer(
            "Заявка не найдена",
            show_alert=True
        )

        return

    await callback.message.answer(
        f"Редактирование заявки №{order_id}",
        reply_markup=edit_keyboard(order_id)
    )

    await callback.answer()

@router.callback_query(
    F.data.startswith("edit_price_")
)
async def edit_price(
    callback: CallbackQuery,
    state: FSMContext
):

    order_id = int(
        callback.data.replace(
            "edit_price_",
            ""
        )
    )

    await state.update_data(
        order_id=order_id
    )

    await state.set_state(
        EditOrderState.editing_price
    )

    await callback.message.answer(
        "Введите новую стоимость"
    )

    await callback.answer()

@router.message(
    EditOrderState.editing_price
)
async def save_price(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    await update_order_field(
        data["order_id"],
        "price",
        message.text
    )
    await refresh_order_message(
        message.bot,
        data["order_id"]
    )

    await message.answer(
        "✅ Стоимость изменена"
    )

    await state.clear()

@router.callback_query(
    F.data.startswith("edit_client_")
)
async def edit_client(
    callback: CallbackQuery,
    state: FSMContext
):

    order_id = int(
        callback.data.replace(
            "edit_client_",
            ""
        )
    )

    await state.update_data(
        order_id=order_id
    )

    await state.set_state(
        EditOrderState.editing_client
    )

    await callback.message.answer(
        "Введите новое имя клиента"
    )

    await callback.answer()

@router.message(
    EditOrderState.editing_client
)
async def save_client(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    await update_order_field(
        data["order_id"],
        "client_name",
        message.text
    )
    await refresh_order_message(
        message.bot,
        data["order_id"]
    )

    await message.answer(
        "✅ Клиент изменён"
    )

    await state.clear()

@router.callback_query(
    F.data.startswith("edit_phone_")
)
async def edit_phone(
    callback: CallbackQuery,
    state: FSMContext
):

    order_id = int(
        callback.data.replace(
            "edit_phone_",
            ""
        )
    )

    await state.update_data(
        order_id=order_id
    )

    await state.set_state(
        EditOrderState.editing_phone
    )

    await callback.message.answer(
        "Введите новый телефон"
    )

    await callback.answer()

@router.message(
    EditOrderState.editing_phone
)
async def save_phone(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    await update_order_field(
        data["order_id"],
        "client_phone",
        message.text
    )
    await refresh_order_message(
        message.bot,
        data["order_id"]
    )

    await message.answer(
        "✅ Телефон изменён"
    )

    await state.clear()

@router.callback_query(
    F.data.startswith("edit_address_")
)
async def edit_address(
    callback: CallbackQuery,
    state: FSMContext
):

    order_id = int(
        callback.data.replace(
            "edit_address_",
            ""
        )
    )

    await state.update_data(
        order_id=order_id
    )

    await state.set_state(
        EditOrderState.editing_address
    )

    await callback.message.answer(
        "Введите новый адрес"
    )

    await callback.answer()

@router.message(
    EditOrderState.editing_address
)
async def save_address(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    await update_order_field(
        data["order_id"],
        "address",
        message.text
    )
    await refresh_order_message(
        message.bot,
        data["order_id"]
    )

    await message.answer(
        "✅ Адрес изменён"
    )

    await state.clear()

@router.callback_query(
    F.data.startswith("edit_comment_")
)
async def edit_comment(
    callback: CallbackQuery,
    state: FSMContext
):

    order_id = int(
        callback.data.replace(
            "edit_comment_",
            ""
        )
    )

    await state.update_data(
        order_id=order_id
    )

    await state.set_state(
        EditOrderState.editing_comment
    )

    await callback.message.answer(
        "Введите новый комментарий"
    )

    await callback.answer()

@router.message(
    EditOrderState.editing_comment
)
async def save_comment(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    await update_order_field(
        data["order_id"],
        "comment",
        message.text
    )
    await refresh_order_message(
        message.bot,
        data["order_id"]
    )

    await message.answer(
        "✅ Комментарий изменён"
    )

    await state.clear()

async def refresh_order_message(
    bot: Bot,
    order_id: int
):

    order = await get_order(order_id)

    if not order:
        return

    text = build_order_text_from_db(order)

    keyboard = order_chat_keyboard(order_id)

    try:

        if order["photos"]:

            await bot.edit_message_caption(
                chat_id=order["chat_id"],
                message_id=order["message_id"],
                caption=text,
                reply_markup=keyboard
            )

        else:

            await bot.edit_message_text(
                chat_id=order["chat_id"],
                message_id=order["message_id"],
                text=text,
                reply_markup=keyboard
            )

    except Exception as e:
        print(e)

@router.callback_query(
    F.data.startswith("move_")
)
async def move_start(
    callback: CallbackQuery,
    state: FSMContext
):

    order_id = int(
        callback.data.replace(
            "move_",
            ""
        )
    )

    dates = await get_order_dates()

    await state.update_data(
        order_id=order_id
    )

    await state.set_state(
        EditOrderState.moving_date
    )

    await callback.message.answer(
        "Выберите новую дату",
        reply_markup=build_dates_keyboard(
            dates,
            prefix="move_date"
        )
    )

    await callback.answer()

@router.callback_query(
    EditOrderState.moving_date,
    F.data.startswith("move_date_")
)
async def move_choose_date(
    callback: CallbackQuery,
    state: FSMContext
):

    date = callback.data.replace(
        "move_date_",
        ""
    )

    await state.update_data(
        new_date=date
    )

    times = await get_order_times(
        date
    )

    await state.set_state(
        EditOrderState.moving_time
    )

    await callback.message.edit_text(
        f"📅 {date}\n\nВыберите время",
        reply_markup=build_times_keyboard(
            times,
            prefix="move_time"
        )
    )

    await callback.answer()

@router.callback_query(
    EditOrderState.moving_time,
    F.data.startswith("move_time_")
)
async def move_finish(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    new_time = callback.data.replace(
        "move_time_",
        ""
    )

    order = await move_order(
        data["order_id"],
        data["new_date"],
        new_time
    )

    await refresh_order_message(
        callback.bot,
        data["order_id"]
    )

    await callback.message.answer(
        "✅ Заявка перенесена"
    )

    await state.clear()

    await callback.answer()