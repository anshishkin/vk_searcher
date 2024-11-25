import logging
from core import config

from aiogram import F, Router
from aiogram.types import Message
from .buttons.buttons import UNBAN_MARKUP

common_router = Router(name="common_router")


@common_router.message(F.from_user.id.in_(config.BAN_LIST))
async def ban_handler(msg: Message):
    logging.getLogger().info("User found in ban_list.")
    await msg.answer(
        "Доступ запрещен. Пользователь забанен.😞 (Для теста разбан с помощью /unban)", reply_markup=UNBAN_MARKUP
    )


@common_router.message(~F.from_user.id.in_(config.USER_ID_LIST))
async def user_not_found_handler(msg: Message):
    logging.getLogger().info("User not found in list")
    await msg.answer("Доступ запрещен.")
