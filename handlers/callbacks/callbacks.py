from aiogram.filters.callback_data import CallbackData
from typing import TypeVar


class FileListCallback(CallbackData, prefix="fl"):
    last_index: int = 10
    first_index: int = 0
    name: str = "files"


class RestartFileCallback(CallbackData, prefix="rf"):
    uuid: str
    name: str


class InfoCallback(CallbackData, prefix="i"):
    name: str = "info"


class SettingsCallback(CallbackData, prefix="set"):
    name: str = "settings"


class UnbanCallback(CallbackData, prefix="unb"):
    name: str = "unban"


class DownloadDataCallback(CallbackData, prefix="db"):
    source: str
    file: str
