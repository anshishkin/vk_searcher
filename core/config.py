from enum import Enum
from dataclasses import dataclass

### Telegram Bot
BAN_LIST = []
USER_ID_LIST = {202583036, 376462955, 5437767305, 140532063, 329281650, 153170925, 435346233, 20258303}
DEFAULT_BAN_TIME_IN_MINUTES = 1

# default config csv
DEFAULT_CSV_SEP = ";"
DEFAULT_CSV_ENCODING = "utf-8"
DEFAULT_CSV_INDEX = False


@dataclass
class VKConfig:
    auth = [
        {"login": "a.shishkin.spb@gmail.com", "password": "c2e9Cf33"},
        {"login": "shisha19@yandex.ru", "password": "c2e9Cf33"},
    ]
    service_token = "a2e56949a2e56949a2e56949a8a1c6d992aa2e5a2e56949c5d6faedd39ec1464411899c"
    proxies = None  # ["http://178.208.181.102:45710:07LWESLQ:T1SH6QC1", "http://77.93.150.37:48092:07LWESLQ:T1SH6QC1"]
    session_verify = True
    limit_requests = 15
    time_period = 3600
