import datetime

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import Message
from aiogram.types import CallbackQuery

from states.book import AddBookState
from db.database import get_async_session
from services.book import BookService
from keyboards.inline_chose_genre import chose_genre_inline_keyboard

router = Router()


@router.message(
    Command("add_book"),
    StateFilter(default_state),
    F.text,
)
async def cmd_add_book(
    message: Message,
    state: FSMContext,
):
    await message.answer(
        text="Пожалуйста, введите название книги.",
    )
    await state.set_state(
        AddBookState.book_title,
    )


@router.message(
    Command("cancel"),
    StateFilter(default_state),
)
async def cancel_add_book_state(
    message: Message,
    state: FSMContext,
):
    await message.answer(
        text="Вы отменили добавление книги",
    )
    await state.clear()


@router.message(
    StateFilter(
        AddBookState.book_title,
    ),
    F.text,
)
async def add_book_title_handler(
    message: Message,
    state: FSMContext,
):
    await state.update_data(
        book_title=message.text,
    )
    await message.answer(
        text="Пожалуйста, опишите книгу.",
    )
    await state.set_state(
        AddBookState.book_description,
    )


@router.message(
    StateFilter(
        AddBookState.book_description,
    ),
    F.text,
)
async def add_book_description_handler(
    message: Message,
    state: FSMContext,
):
    await state.update_data(book_description=message.text)

    keyboard = await chose_genre_inline_keyboard()
    await message.answer(
        text="Пожалуйста, выберите жанр книги:",
        reply_markup=keyboard,
    )
    await state.set_state(
        AddBookState.book_genre,
    )


@router.callback_query(
    AddBookState.book_genre,
    F.data.startswith("genre:"),
)
async def process_genre_selection(
    callback: CallbackQuery,
    state: FSMContext,
):
    genre_id = int(callback.data.split(":")[1])
    await state.update_data(genre=genre_id)

    await callback.message.edit_text(
        text="Жанр выбран. Пожалуйста, введите год написания книги."
    )
    await callback.answer()

    await state.set_state(
        AddBookState.book_year,
    )


@router.message(
    StateFilter(AddBookState.book_year),
    F.text.func(
        lambda text: text.isdigit() and 0 < int(text) <= datetime.datetime.now().year
    ),
)
async def add_book_year_handler(
    message: Message,
    state: FSMContext,
):
    year_int = int(message.text)
    await state.update_data(book_year=year_int)
    await message.answer(
        text="Пожалуйста, введите имя автора.",
    )
    await state.set_state(
        AddBookState.author_first_name,
    )


@router.message(
    StateFilter(AddBookState.book_year),
)
async def invalid_year_handler(
    message: Message,
):
    current_year = datetime.datetime.now().year
    await message.answer(
        text=f"Пожалуйста, введите корректный год (от 1 до {current_year}).",
    )


@router.message(
    StateFilter(AddBookState.author_first_name),
    F.text,
)
async def add_author_first_name_handler(
    message: Message,
    state: FSMContext,
):
    await state.update_data(author_first_name=message.text)
    await message.answer(
        text="Пожалуйста, введите фамилию автора.",
    )
    await state.set_state(AddBookState.author_last_name)


@router.message(
    StateFilter(AddBookState.author_last_name),
    F.text,
)
async def add_author_last_name_handler(
    message: Message,
    state: FSMContext,
):
    await state.update_data(author_last_name=message.text)
    await message.answer(
        text="Пожалуйста, введите отчество автора(если есть, или напишите 'нет').",
    )
    await state.set_state(AddBookState.author_patronymic)


@router.message(
    StateFilter(
        AddBookState.author_patronymic,
    ),
    F.text,
)
async def add_author_patronymic_handler(
    message: Message,
    state: FSMContext,
):
    await state.update_data(
        author_patronymic=message.text,
    )

    data = await state.get_data()

    book_name = data.get("book_title")
    book_description = data.get("book_description")
    book_genre = data.get("genre")
    book_year = data.get("book_year")
    author_first_name = data.get("author_first_name")
    author_last_name = data.get("author_last_name")
    author_patronymic = data.get("author_patronymic")

    session = await get_async_session()
    book_service = BookService(session)

    result = book_service.add_book(
        book_title=book_name,
        book_dedcription=book_description,
        book_genre=book_genre,
        book_year=book_year,
        author_first_name=author_first_name,
        author_last_name=author_last_name,
        author_patronymic=author_patronymic,
        )
    
    if result:
        await message.answer(
            text="Спасибо. Книга добавлена.",
            )
    else:
        await message.answer(
            text=(
                "Произошла ошибка при дабовлении книги.", 
                "Попробуйте ещё раз.",
                ),
            )

    await state.clear()
