from aiogram.fsm.state import State, StatesGroup


class UserRegister(StatesGroup):
    enter_first_name = State()
    enter_last_name = State()
