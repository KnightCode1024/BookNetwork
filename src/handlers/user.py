from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from db.database import get_async_session
# from db.repositories.user import UserRepository
from services.user import UserService


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    first_name = user.first_name
    last_name = user.last_name
    username = "@" + user.username if user.username else None
    tg_id = user.id

    session = await get_async_session()
    user_service = UserService(session)

    result = await user_service.register_or_update_user(
        tg_id=tg_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
    if result["action"] == "created":
        await message.answer(
            text="Вы успешно зарегистрировались!",
        )
    elif result["action"] == "updated":
        await message.answer(text="Мы обнавмли ваши данные.")

    else:
        await message.answer(text="Рады видеть вас снова!")
