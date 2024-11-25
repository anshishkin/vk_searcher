from ..callbacks.callbacks import FileListCallback, SettingsCallback, InfoCallback, UnbanCallback
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

UNBAN_MARKUP = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Разбаниться", callback_data=UnbanCallback().pack())]]
)

DEFAULT_MARKUP = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📞 Телефон", callback_data=InfoCallback().pack()),
            InlineKeyboardButton(text="+79530000018", callback_data=InfoCallback().pack()),
        ],
        [
            InlineKeyboardButton(text="🆔 ID VK", callback_data=InfoCallback().pack()),
            InlineKeyboardButton(text="id6799642", callback_data=InfoCallback().pack()),
        ],
        [
            InlineKeyboardButton(text="📧 Почта ", callback_data=InfoCallback().pack()),
            InlineKeyboardButton(text="example@gmail.com", callback_data=InfoCallback().pack()),
        ],
        [
            InlineKeyboardButton(text="🧖🏼‍♂️ Фамалия Имя", callback_data=InfoCallback().pack()),
            InlineKeyboardButton(text="Иванов Иван", callback_data=InfoCallback().pack()),
        ],
    ]
)
