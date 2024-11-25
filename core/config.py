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

DEFAULT_TEMP_PATH = "./temp"


@dataclass
class VKConfig:
    login = "a.shishkin.spb@gmail.com"
    password = "c2e9Cf33"
    service_token = "a2e56949a2e56949a2e56949a8a1c6d992aa2e5a2e56949c5d6faedd39ec1464411899c"
    proxies = ["http://178.208.181.102:45710:07LWESLQ:T1SH6QC1", "http://77.93.150.37:48092:07LWESLQ:T1SH6QC1"]


@dataclass
class OPENAIConfig:
    model: str = "gpt-4o"
    proxy_url: str = "http://07LWESLQ:T1SH6QC1@178.208.181.102:45710"  # "http://UzJjHwPn:ebqzEctc@185.244.161.86:62270"
    temperature: int = 0
    api_key: str = "sk-LgfIcv2C8eVrVZQX158X9ZUVC7xqU2ZH1TAD4OPEzKT3BlbkFJhFZLeQlsZ4qtzkD-3VS1vPBspJzIemekWIHGdTMQwA"
