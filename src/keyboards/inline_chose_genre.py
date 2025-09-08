from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.genre import GenreService
from db.database import get_async_session


async def chose_genre_inline_keyboard():
    builder = InlineKeyboardBuilder()

    session = await get_async_session()
    genre_service = GenreService(session)

    genres = await genre_service.get_all_genres()

    for genre in genres:
        builder.button(
            text=genre.name,
            callback_data=f"genre:{genre.id}"
        )

    builder.button(text="Отменить", callback_data="cancel")
    builder.adjust(2, 2)

    return builder.as_markup()
