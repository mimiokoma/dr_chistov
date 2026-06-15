from datetime import datetime

from states.slot_states import DeleteSlotsState

from database.requests import (
    get_available_dates,
    get_slots_by_date,
    delete_slots
)

from keyboards.slots import (
    build_delete_dates_keyboard,
    build_delete_slots_keyboard
)

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.slots import slots_menu
from utils.calendar import build_calendar

from aiogram.fsm.context import FSMContext

from database.requests import save_slots

from keyboards.slots import build_time_keyboard

from database.requests import get_all_slots

router = Router()


@router.message(F.text == "📅 Управление датами")
async def manage_slots(message: Message):

    await message.answer(
        "Управление слотами",
        reply_markup=slots_menu
    )


@router.callback_query(F.data == "add_slots")
async def add_slots(callback: CallbackQuery):

    now = datetime.now()

    await callback.message.edit_text(
        "Выберите дату",
        reply_markup=build_calendar(
            now.year,
            now.month
        )
    )

    await callback.answer()


@router.callback_query(F.data == "delete_slots")
async def delete_slots_menu(
        callback: CallbackQuery
):

    dates = await get_available_dates()

    if not dates:

        await callback.answer(
            "Свободных слотов нет",
            show_alert=True
        )
        return

    await callback.message.edit_text(
        "Выберите дату",
        reply_markup=
        build_delete_dates_keyboard(
            dates
        )
    )

    await callback.answer()


@router.callback_query(F.data == "all_slots")
async def all_slots(callback: CallbackQuery):

    slots = await get_all_slots()

    if not slots:

        await callback.message.edit_text(
            "Слотов пока нет"
        )

        await callback.answer()
        return

    result = "📋 Все слоты\n\n"

    current_date = None

    for date, time in slots:

        if current_date != date:

            current_date = date

            result += (
                f"\n📅 {date}\n"
            )

        result += f"• {time}\n"

    await callback.message.edit_text(
        result
    )

    await callback.answer()

@router.callback_query(F.data.startswith("month_"))
async def change_month(callback: CallbackQuery):

    _, month, year = callback.data.split("_")

    await callback.message.edit_reply_markup(
        reply_markup=build_calendar(
            int(year),
            int(month)
        )
    )

    await callback.answer()

@router.callback_query(F.data.startswith("date_"))
async def select_date(
        callback: CallbackQuery,
        state: FSMContext
):

    _, day, month, year = callback.data.split("_")

    selected_date = (
        f"{day.zfill(2)}."
        f"{month.zfill(2)}."
        f"{year}"
    )

    await state.update_data(
        selected_date=selected_date,
        selected_times=[]
    )

    await callback.message.edit_text(
        f"📅 {selected_date}\n\nВыберите время",
        reply_markup=build_time_keyboard([])
    )

    await callback.answer()

@router.callback_query(F.data.startswith("time_"))
async def select_time(
        callback: CallbackQuery,
        state: FSMContext
):

    selected_time = callback.data.replace(
        "time_",
        ""
    )

    data = await state.get_data()

    selected_times = data.get(
        "selected_times",
        []
    )

    if selected_time in selected_times:
        selected_times.remove(
            selected_time
        )
    else:
        selected_times.append(
            selected_time
        )

    await state.update_data(
        selected_times=selected_times
    )

    date = data["selected_date"]

    await callback.message.edit_text(
        f"📅 {date}\n\nВыберите время",
        reply_markup=build_time_keyboard(
            selected_times
        )
    )

    await callback.answer()

@router.callback_query(F.data == "save_slots")
async def save_selected_slots(
        callback: CallbackQuery,
        state: FSMContext
):

    data = await state.get_data()

    date = data.get("selected_date")

    selected_times = data.get(
        "selected_times",
        []
    )

    if not selected_times:

        await callback.answer(
            "Выберите хотя бы один слот",
            show_alert=True
        )

        return

    added_count = await save_slots(
        date,
        selected_times
    )

    times_text = "\n".join(
        sorted(selected_times)
    )

    await state.clear()

    await callback.message.edit_text(
        f"✅ Добавлено слотов: {added_count}\n\n"
        f"📅 {date}\n\n"
        f"{times_text}"
    )

    await callback.answer()

@router.callback_query(
    F.data.startswith("delete_date_")
)
async def choose_delete_date(
        callback: CallbackQuery,
        state: FSMContext
):

    date = callback.data.replace(
        "delete_date_",
        ""
    )

    slots = await get_slots_by_date(
        date
    )

    await state.update_data(
        delete_date=date,
        delete_ids=[]
    )

    await callback.message.edit_text(
        f"📅 {date}\n\n"
        f"Выберите слоты для удаления",
        reply_markup=
        build_delete_slots_keyboard(
            slots,
            []
        )
    )

    await callback.answer()

@router.callback_query(
    F.data.startswith("delslot_")
)
async def toggle_delete_slot(
        callback: CallbackQuery,
        state: FSMContext
):

    slot_id = int(
        callback.data.replace(
            "delslot_",
            ""
        )
    )

    data = await state.get_data()

    selected_ids = data.get(
        "delete_ids",
        []
    )

    if slot_id in selected_ids:
        selected_ids.remove(slot_id)
    else:
        selected_ids.append(slot_id)

    await state.update_data(
        delete_ids=selected_ids
    )

    slots = await get_slots_by_date(
        data["delete_date"]
    )

    await callback.message.edit_reply_markup(
        reply_markup=
        build_delete_slots_keyboard(
            slots,
            selected_ids
        )
    )

    await callback.answer()

@router.callback_query(
    F.data == "confirm_delete_slots"
)
async def confirm_delete_slots(
        callback: CallbackQuery,
        state: FSMContext
):

    data = await state.get_data()

    ids = data.get(
        "delete_ids",
        []
    )

    if not ids:

        await callback.answer(
            "Ничего не выбрано",
            show_alert=True
        )
        return

    await delete_slots(ids)

    count = len(ids)

    await state.clear()

    await callback.message.edit_text(
        f"🗑 Удалено слотов: {count}"
    )

    await callback.answer()