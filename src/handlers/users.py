from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    first_name = user.first_name
    last_name = user.last_name
    username = "@" + user.username if user.username else None
    tg_id = user.id

    await message.answer(
        f"Здравствуйте, {first_name}!\nЯ бот библиотекарь.\n"
        "Я знаю о вас:\n"
        f"Имя: {first_name}\n"
        f"Фамилия: {last_name}\n"
        f"Юзернейм: {username}\n"
        f"ID: {tg_id}\n"
    )
