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