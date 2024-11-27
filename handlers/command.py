import logging
import os

from core import config
from .buttons.buttons import UNBAN_MARKUP, DEFAULT_MARKUP
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.filters.command import CommandObject
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from .callbacks.callbacks import DownloadDataCallback
import uuid
from searcher.vk import VKSearcher
from aiogram.types.input_file import FSInputFile
import pandas as pd
import re
from aiogram.enums import ParseMode
from pathlib import Path
import random

DEFAULT_TEMP_PATH = os.getenv("DEFAULT_TEMP_PATH")

path = Path(__file__).parent.parent.absolute()
Path(str(path) + DEFAULT_TEMP_PATH).mkdir(parents=True, exist_ok=True)

vkInstance = VKSearcher(config.VKConfig)

command_router = Router(name="command_router")


@command_router.message(CommandStart(), F.from_user.id.in_(config.USER_ID_LIST))
async def start_handler(message: Message):
    logging.info("ID пользователя найден в списке id. Доступ разрешен.")
    await message.answer(
        text=f"Добро пожаловать в тестовую версию поиского бота VK! \n <b>Примеры команд для поиска 👇:</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=DEFAULT_MARKUP,
    )


@command_router.callback_query(DownloadDataCallback.filter(F.source == "vk"), F.from_user.id.in_(config.USER_ID_LIST))
async def download_handler(callback_query: CallbackQuery, callback_data: DownloadDataCallback):
    path = f".{DEFAULT_TEMP_PATH}/{callback_data.file}.csv"
    await callback_query.message.answer_document(document=FSInputFile(path))
    os.system(f"rm {path}")


@command_router.message(Command("restart"), F.from_user.id.in_(config.USER_ID_LIST))
async def restart_handler(message: Message, command: CommandObject):
    logging.getLogger().info(f"Command: {message.text}")
    user_id = message.from_user.id
    message_text = "Комманда выполнена успешно."
    logging.getLogger().info("Command finished. Sending message.")
    await message.answer(message_text, reply_markup=DEFAULT_MARKUP)


@command_router.message(F.text, F.from_user.id.in_(config.USER_ID_LIST))
async def found_data_handler(msg: Message):
    # reply = None
    format_parsedData = {}
    parsedData = {}
    info_text = str()
    # is_api= False
    msg_text = msg.text
    if re.match("^((\+7|\+8|7|8)*(9)+([0-9]){9})$", msg_text):
        phone_numbers = msg_text
        if phone_numbers.startswith("9"):
            phone_numbers = "+7" + phone_numbers

        try:
            parsedData = vkInstance.get_result(phone_numbers=[phone_numbers])
            if parsedData[phone_numbers]["found"]:
                tmp = parsedData[phone_numbers]
                vk_id = parsedData[phone_numbers]["id"]
                tmp.update({"vkontakte_url": f"https://vk.com/id{vk_id}"})
                parsedData[phone_numbers] = tmp
                # df = pd.DataFrame.from_dict(parsedData, orient='index')
                # df['phone_number'] = df.index
                # is_api = True
            else:
                await msg.answer(f" ℹ️ Пользователь, которого вы ищете, запретил поиск через импорт контактов")
        except:
            await msg.answer(
                f"🚫 Сервис API VK не доступен \n ℹ️ Попробуйте через несколько часов или обратитесь к администратору"
            )
            parsedData[phone_numbers] = {"found": False}
        finally:
            if not parsedData[phone_numbers]["found"]:
                # phone_numbers = re.sub('[^A-Za-z0-9]+',"",phone_numbers)
                df = vkInstance.profile_parser_db(f"phone_number.like('%{phone_numbers[-10:]}%')")
                if len(df) > 0:
                    tmp = {"found": True}
                    tmp.update(df.iloc[:, 1:].to_dict("records")[0])
                    # df.rename(columns={"vkontakte_id":"vk_id"})
                    parsedData[phone_numbers] = tmp
            if parsedData[phone_numbers]["found"]:
                uuid_hex = uuid.uuid4().hex
                df_fin = pd.DataFrame.from_dict(parsedData, orient="index")
                df_fin["phone_number"] = phone_numbers
                df_fin.iloc[:, 1:].to_csv(
                    path_or_buf=f".{DEFAULT_TEMP_PATH}/{uuid_hex}.csv", sep=",", encoding="utf-8", index=False
                )
                button = InlineKeyboardButton(
                    text=" ✔️ Скачать", callback_data=DownloadDataCallback(source="vk", file=uuid_hex).pack()
                )
                reply = InlineKeyboardMarkup(inline_keyboard=[[button]])
                for key, value in parsedData[phone_numbers].items():
                    if key not in ["found", "phone_number"]:
                        info_text += f"▫️ <b>{key}</b>: {value} \n"
                await msg.answer(f"Поиск ВК по номеру <b>{phone_numbers}</b> 👇:\n{info_text} ", reply_markup=reply)
            else:
                await msg.answer(f"К сожалению, мы ничего не нашли 😞...")
    elif "id" in msg_text:
        vk_id = msg_text.split("id")[1]
        if vk_id.isdigit():
            try:
                parsedData = vkInstance.get_profile_by_token(vk_id)
            except:
                await msg.answer(
                    f"🚫 Сервис API VK не доступен \n ℹ️ Попробуйте через несколько часов или обратитесь к администратору"
                )

            df = vkInstance.profile_parser_db(f"vkontakte_id=={vk_id}")
            if len(df) > 0:
                if not parsedData:
                    parsedData = df.iloc[:, 2:].to_dict("records")[0]
                else:
                    if "deactivated" in parsedData.keys():
                        parsedData = df.iloc[:, 2:].to_dict("records")[0]
                    else:
                        parsedData["phone_number"] = df.phone_number.values[0]

            if parsedData:
                for key in parsedData.keys():
                    if key == "sex":
                        parsedData["sex"] = "male" if parsedData["sex"] == 2 else "female"
                    if key == "city":
                        parsedData["city"] = parsedData["city"]["title"]
                parsedData["vkontakte_url"] = f"https://vk.com/id{vk_id}"
                uuid_hex = uuid.uuid4().hex
                format_parsedData[vk_id] = parsedData
                df_fin = pd.DataFrame.from_dict(format_parsedData, orient="index")
                df_fin.drop(["can_access_closed", "is_closed"], axis=1).to_csv(
                    path_or_buf=f".{DEFAULT_TEMP_PATH}/{uuid_hex}.csv", sep=",", encoding="utf-8", index=False
                )
                button = InlineKeyboardButton(
                    text=" ✔️ Скачать", callback_data=DownloadDataCallback(source="vk", file=uuid_hex).pack()
                )
                reply = InlineKeyboardMarkup(inline_keyboard=[[button]])
                for key, value in format_parsedData[vk_id].items():
                    if key not in ["can_access_closed", "is_closed", "vkontakte_id"]:
                        info_text += f"▫️ <b>{key}</b>: {value} \n"

                await msg.answer(f"Поиск ВК по ID <b>{vk_id}</b> 👇:\n{info_text} ", reply_markup=reply)
            else:
                await msg.answer(f"Пользователя с таким id не найден 😞...")
        else:
            await msg.answer(
                f"❌ Нечисловой формат ID \n ℹ️ Введите корректно численное значение после id, например: id44444"
            )
    else:
        await msg.answer(f"❌ Неверный формат ввода данных \n ℹ️ Введите, например: +79819408810 или id616661")
