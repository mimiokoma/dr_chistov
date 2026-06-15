from aiogram.fsm.state import State, StatesGroup


class SlotSelection(StatesGroup):
    choosing_time = State()

from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class DeleteSlotsState(StatesGroup):
    choosing_slots = State()