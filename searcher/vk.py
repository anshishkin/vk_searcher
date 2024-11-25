import requests
import json
import urllib
import hashlib
import uuid
import random
from abc import ABC
import yaml
import uuid
from abc import ABC
import sqlalchemy as sa
from sqlalchemy import or_
from sqlalchemy.inspection import inspect
from .exceptions import *
from urllib3.exceptions import MaxRetryError, NewConnectionError
from socket import gaierror
from urllib.parse import urlparse
from time import time
import pandas as pd
import logging
from db.postgres.orm import Session, engine, VK_Contact

logger = logging.getLogger(__name__)
with open("core/vk_config.yaml") as stream:
    templates = yaml.safe_load(stream)

def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped   

class VKSearcher(ABC):
    android_resolution = "1200x1290"  # ['1024x600', '1280x800', '480x854', '720x1280', '1200x1290', '2560x1600', '768x1280', '1080x1920','800x1280']
    android_sdk = "30"  # [{'sdkVersion':'28','androidVersion':'9'},{'sdkVersion':'29','androidVersion':'10'},{'sdkVersion':'30','androidVersion':'11'},{'sdkVersion':'31','androidVersion':'12'},{'sdkVersion':'33','androidVersion':'13'}]
    android_version = "11"
    android_model = "SM-A515"  # ['SM-A505F','SM-A515','SM-A516F','SM-A526B','SM-A710F','SM-A530F']
    limit = 3

    def __init__(self, proxies: list = None, sessionVerify: bool = True):
        self.session = requests.session()
        self.proxies = proxies
        self.start_time = time()
        if self.proxies is not None:
            proxy = random.choice(self.proxies)
            self.set_proxy(proxy, sessionVerify)

    def set_proxy(self, proxy, session_verify):
        self.session.verify = session_verify
        if proxy:
            assert isinstance(proxy, str), f"Proxy must be string format, but now its {type(proxy)}"
            proxy_href = "{scheme}{href}".format(
                scheme="http://" if not urlparse(proxy).scheme else "",
                href=proxy,
            )
            self.session.proxies = {
                "http": proxy_href,
                "https": proxy_href,
            }

    def login(self, username: str, password: str):
        self.username = username
        self.password = password
        self.generate_init()

    def generate_init(self):
        self.useragent = f"VKAndroidApp/7.24-3439 (Android {self.android_version}; SDK {self.android_sdk}; armeabi-v7a; samsung {self.android_model}; ru; {self.android_resolution})"
        self.device_uuid = str(uuid.uuid4())

        # DeviceHash
        seed = hashlib.md5(self.username.encode("utf-8") + self.password.encode("utf-8")).hexdigest()
        m = hashlib.md5()
        m.update(seed.encode("utf-8"))
        device_hash = m.hexdigest()[:16]

        # authData
        auth_headers = {"Host": "oauth.vk.com", "User-Agent": self.useragent}

        auth_params = {
            "scope": "nohttps,all",
            "client_id": "2274003",  #'52614274', #,'52670683' ,#,
            "client_secret": "hHbZxrka2uZ6jB1inYsH",  #'0JQnKPwykvpxjdYpQDFp', #'rPZzldkSVdM6onBo343j', #,  # apps secret token - static
            "v": "5.96",
            "lang": "ru",
            "2fa_supported": "1",
            "lang": "ru",
            "device_id": device_hash,
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "libverify_support": "0",
        }
        self.auth_parser(
            self.session.get("https://oauth.vk.com/token", params=auth_params, headers=auth_headers).json()
        )
    
    def is_possible_requests(self):
        current_time = time()
        #print(self.search_contact.calls)
        if self.__class__.search_contact.calls < self.limit:
            return True
        elif current_time - self.start_time > 30:
            self.start_time = current_time
            self.refresh_param()
            self.__class__.search_contact.calls  = 0
            return True
        else:
            return False

    def refresh_param(self):
        if self.proxies is not None and len(self.proxies) > 1:
            proxy = random.choice(self.proxies)
            while self.session.proxies.values() == proxy:
                proxy = random.choice(self.proxies)
            self.change_proxy(proxy)
        self.update_tokens()

    def update_tokens_parser(self, tokens_data):
        self.accessToken = tokens_data["response"]["token"]
        self.secret = tokens_data["response"]["secret"]

    def change_proxy(self, proxy: str, session_verify: bool = True):
        self.set_proxy(proxy, session_verify)

    def update_tokens(self):
        data = {
            "v": "5.96",
            "https": "1",
            "timestamp": "0",
            "receipt2": "eyJhbGciOiAibm9uZSJ9.eyJub25jZSI6ICJ0ZXN0PT0ifQ.",
            "device_id": self.device_uuid,
            "receipt": "yssp9o9p9pamz5t-nvmq8spgwtin3e0==",
            "lang": "ru",
            "access_token": self.access_token,
        }

        tokens_data = self.makeRequest("auth.refreshToken", data)
        self.update_tokens_parser(tokens_data)

    def get_result(self, phone_numbers: list):
        self.parsed_data = {}
        for self.phone_number in phone_numbers:
            self.profile_data = {}
            self.search_contact()
            self.contact_parser()
            if self.found:
                self.get_profile()
            self.profile_parser_api()
        return self.parsed_data
    
    @counted
    def search_contact(self):
        if self.is_possible_requests():
            contacts = {"phone": {"user_contact": self.username, "contacts": self.phone_number}}
            data = {
                "v": "5.96",
                "https": "1",
                "device_id": self.device_uuid,
                "fields": "online,photo_50,photo_100,photo_200,career,city,country,education,verified,trending",
                "lang": "ru",
                "search_only": "0",
                "count": "5000",
                "contacts": json.dumps(contacts, separators=(",", ":")),
                "need_mutual": "1",
                "access_token": self.access_token,
            }
            contact_data = self.make_request("account.searchContacts", data)
            self.contact_data = contact_data
        else:
            raise LimitError("Requests limits reached")

    def get_profile(self):
        data = {
            "v": "5.96",
            "https": "1",
            "track_code": self.track_code,
            "source": "friends_import_address_book",
            "gift_count": "25",
            "track_events": "1",
            "skip_hidden": "1",
            "photo_sizes": "1",
            "func_v": "8",
            "access_keys": self.access_key,
            "device_id": self.device_uuid,
            "photo_count": "25",
            "lang": "ru",
            "ref": "profile",
            "user_id": self.user_id,
            "access_token": self.access_token,
        }
        self.profile_data = self.make_request("execute.getFullProfileNewNew", data)

    def get_user_profile(self, user_id):
        data = {
            "user_id": user_id,
            "is_owner": "0",
            #'privacy_section': 'stories, audios',
            "is_photo_feed": "1",
            "nfts_limit": "15",
            "is_nft_request_updated": "0",
            "func_v": "8",
            "lang": "ru",
            "device_id": self.device_uuid,
            "v": "5.96",
            "https": "1",
            "access_token": self.access_token,
        }

        self.profile_user = self.make_request("execute.getUserProfileContent", data)

    def make_request(self, method, data):

        base_headers = {
            "Host": "api.vk.com",
            "Cache-Control": "no-cache",
            "User-Agent": self.useragent,
            "X-Vk-Android-Client": "new",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        }

        sig_str = f"/method/{method}?" + urllib.parse.unquote(urllib.parse.urlencode(data)) + self.secret
        sig = hashlib.md5(sig_str.encode()).hexdigest()  # Signature generate
        data["sig"] = sig
        try:
            response = self.session.post(f"https://api.vk.com/method/{method}", headers=base_headers, data=data)
            json_resp = response.json()

            if "error" in json_resp:
                if json_resp["error"]["error_code"] == 13:
                    raise LimitError("Requests limist reached")
                elif json_resp["error"]["error_msg"] == "Flood control":
                    raise FloodError("Flood control triggerred, change bot account")
                elif json_resp["error"]["error_msg"] == "Token confirmation required":
                    raise TokenError("Access & Secret tokens expired")
            return json_resp
        except json.decoder.JSONDecodeError:
            raise JsonDecodeError("Error in decoding response json")
        except (requests.exceptions.ProxyError, MaxRetryError, NewConnectionError, gaierror):
            raise ProxyError("Lost connection to server, Inavild proxy")

    def set_tokens(self, auth_data):
        self.access_token = auth_data.get("access_token", None)
        self.secret = auth_data.get("secret", None)
        self.user_id = auth_data.get("user_id", None)

    def auth_parser(self, auth_data):
        if "error_description" in auth_data and auth_data["error_description"] == "Неправильный логин или пароль":
            raise WrongAuthCredientals(
                f"Login or password is incorrect\nLogin : {self.username}\nPassword : {self.password}\n"
            )
        if "access_token" and "user_id" and "secret" in auth_data:
            self.set_tokens(auth_data)
        else:
            print(auth_data)
            raise UnknownError("Unknown Error")

    def contact_parser(self):
        if len(self.contact_data["response"]["found"]):
            contact = self.contact_data["response"]["found"][0]["user"]
            self.track_code = contact["track_code"]
            self.access_key = contact["access_key"]
            self.found = True
        else:
            self.found = False

    def profile_parser_api(self):
        self.parsed_data[self.phone_number] = {"found": self.found}
        if self.found:
            for key, value in templates.items():
                try:
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            self.parsed_data[self.phone_number].update(
                                {key: self.profile_data["response"][sub_key][sub_value]}
                            )
                    else:
                        if value == "sex":
                            gender = "male" if self.profile_data["response"][value] == 2 else "female"
                            self.parsed_data[self.phone_number].update({key: gender})
                        else:
                            self.parsed_data[self.phone_number].update({key: self.profile_data["response"][value]})
                except:
                    continue

    def profile_parser_db(self, call_args: str):
        try:
            with Session.begin() as session:
                query = f"sa.select(VK_Contact).filter(VK_Contact.{call_args})"
                print(query)
                query_result = eval(query)
                df = pd.read_sql_query(query_result, con=engine)
                session.close()
            df_ = df.drop(columns=df.columns[(df == "nan").all()]).dropna(axis=1, how="all")
            return df_
        except:
            return pd.DataFrame([])

    def profile_custom_db(self, call_args: str):
        with Session.begin() as session:
            if "=" in call_args:
                query = f"session.query(VK_Contact).filter_by({call_args}).statement"
                query_result = eval(query)
                df = pd.read_sql_query(query_result, con=engine)
            else:
                columns = [column for column in inspect(VK_Contact).c]
                query_result = session.query(VK_Contact).where(or_(*[col.contains(call_args) for col in columns[2:]]))
                df = pd.read_sql(query_result.statement, con=engine)
            session.close()
        df_ = df.drop(columns=df.columns[(df == "nan").all()]).dropna(axis=1, how="all")
        return df_.iloc[:, 1:]
    
    @counted
    def get_profile_by_token(self, id, token):
        return requests.post(
            "https://api.vk.com/method/users.get",
            params={
                "access_token": token,
                "v": 5.131,
                "user_ids": id,
                "lang": "ru",
                "fields": "bdate,first_name,city,sex,screen_name,country",
            },
        ).json()["response"][0]
