from aiogram.fsm.state import State, StatesGroup


class SlotStates(StatesGroup):
    waiting_for_date = State()
    waiting_for_time = State()

from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class CreateOrder(StatesGroup):

    services = State()

    quantity = State()

    date = State()

    time = State()

    client_name = State()

    client_phone = State()

    address = State()

    source = State()

    price = State()

    comment = State()

    photo = State()

    confirm = State()

class EditOrderState(StatesGroup):

    choosing_field = State()

    editing_price = State()

    editing_client = State()

    editing_phone = State()

    editing_address = State()

    editing_comment = State()

    moving_date = State()

    moving_time = State()