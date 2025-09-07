from aiogram.fsm.state import State, StatesGroup


class AddBookState(StatesGroup):
    """book state for Book model"""

    book_title = State()
    book_description = State()
    book_genre = State()
    book_year = State()

    """author state for Author model"""

    author_first_name = State()
    author_last_name = State()
    author_patronymic = State()
