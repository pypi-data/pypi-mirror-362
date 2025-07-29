#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Author: AnhNT
    Company: MobioVN
    Date created: 26/02/2021

"""

import base64
import datetime
import json

import requests
import time
from dateutil.parser import parse
from jose import jwt
from mobio.libs.Singleton import Singleton
from mobio.libs.caching import LRUCacheDict
from mobio.libs.ciphers import MobioCrypt2
from mobio.libs.kafka_lib.helpers.kafka_producer_manager import KafkaProducerManager

from .aes_cipher import AESCipher

from .config import (
    SystemConfigKeys, UrlConfig, KafkaTopic, lru_redis_cache
)
from .date_utils import ConvertTime
from .mobio_admin_sdk import MobioAdminSDK


def decrypt_data(enc_data):
    try:
        while len(enc_data) % 4 != 0:
            enc_data = enc_data + "="
        decrypt_resp = AESCipher().decrypt(enc_data)
        if decrypt_resp:
            return json.loads(decrypt_resp)
        return None
    except Exception as e:
        print("admin_sdk::decrypt_data: Exception: %s" % e)
        return None


def get_merchant_auth(merchant_id):
    from .call_api import CallAPI
    result = CallAPI.get_merchant_config_host(merchant_id)
    if not result or not result.get("jwt_algorithm") or not result.get("jwt_secret_key"):
        print("admin_sdk::get_merchant_auth: jwt_algorithm None, jwt_secret_key None")
        raise ValueError("admin_sdk::can not get merchant config auth ")
    return {
        SystemConfigKeys.JWT_ALGORITHM: result.get("jwt_algorithm"),
        SystemConfigKeys.JWT_SECRET_KEY: result.get("jwt_secret_key"),
    }


def get_partner_info_decrypt(partner_key, decrypt=False):
    partner_info_enc = get_partner_info_by_key(partner_key)
    if not decrypt:
        return partner_info_enc
    else:
        if not partner_info_enc or not isinstance(partner_info_enc, dict) or not partner_info_enc.get("data"):
            return partner_info_enc
        partner_info_dec = MobioCrypt2.d1(partner_info_enc.get("data"), enc="utf-8")
        return {"code": 200, "data": json.loads(partner_info_dec)}


@lru_redis_cache.add()
def get_partner_info_by_key(partner_key):
    if not partner_key:
        return None
    adm_url = str(UrlConfig.PARTNER_INFO_CIPHER_ENCRYPT).format(
        host=MobioAdminSDK().admin_host,
        version=MobioAdminSDK().admin_version,
        partner_id=partner_key,
    )
    resp = requests.get(
        adm_url,
        headers=MobioAdminSDK().request_header,
        timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    )
    resp.raise_for_status()
    return resp.json()


def check_basic_auth_v2(partner_key):
    try:
        partner_info_enc = get_partner_info_by_key_v2(partner_key)
        if not partner_info_enc:
            return False
        # partner_info_dec = MobioCrypt2.d1(partner_info_enc, enc="utf-8")
        # partner_info = json.loads(partner_info_dec)
        partner_info = decrypt_data(partner_info_enc)
        expire_time = parse(partner_info.get("expired_time"))
        if expire_time.replace(tzinfo=datetime.timezone.utc) < ConvertTime.get_utc_now():
            print("admin_sdk::check_basic_auth: reach expire time: %s" % str(expire_time))
            return False
        return True
    except Exception as e:
        print("admin_sdk::check_basic_auth: error: %s" % e)
        return False


@lru_redis_cache.add()
def get_partner_info_by_key_v2(partner_key):
    if not partner_key:
        return None
    adm_url = str(UrlConfig.PARTNER_INFO).format(
        host=MobioAdminSDK().admin_host,
        version=MobioAdminSDK().admin_version,
        partner_id=partner_key,
    )
    resp = requests.get(
        adm_url,
        headers=MobioAdminSDK().request_header,
        timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    )
    resp.raise_for_status()
    status_code = resp.status_code
    if status_code == 200:
        result = resp.json()
        enc_data = result["data"]
        return enc_data
    else:
        print("admin_sdk::get_expire_time_by_key: error: status_code = %d" % status_code)
        return None


class Base64(object):
    @staticmethod
    def encode(data):
        try:
            byte_string = data.encode("utf-8")
            encoded_data = base64.b64encode(byte_string)
            return encoded_data.decode(encoding="UTF-8")
        except Exception as ex:
            print(ex)
            return ""

    @staticmethod
    def decode(encoded_data):
        try:
            if isinstance(encoded_data, bytes):
                encoded_data = encoded_data.decode("UTF-8")
            decoded_data = base64.urlsafe_b64decode(
                encoded_data + "=" * (-len(encoded_data) % 4)
            )
            return decoded_data.decode(encoding="UTF-8")
        except Exception as ex:
            print(ex)
            return encoded_data


def push_kafka_log_action_account(json_mess):
    if not json_mess:
        raise ValueError("data none")
    if not json_mess.get("account_id"):
        raise ValueError("account_id not found")
    if not json_mess.get("merchant_id"):
        raise ValueError("merchant_id not found")
    if not json_mess.get("created_time"):
        raise ValueError("created_time not found")
    if not json_mess.get("action_name_vi") and not json_mess.get("action_name_en"):
        raise ValueError("action_name_vi and action_name_en not found")
    if not json_mess.get("action_name_vi") and json_mess.get("action_name_en"):
        json_mess["action_name_vi"] = json_mess.get("action_name_en")
    if json_mess.get("action_name_vi") and not json_mess.get("action_name_en"):
        json_mess["action_name_en"] = json_mess.get("action_name_vi")
    json_mess["source"] = "admin_sdk"
    push_message_kafka(
        topic=KafkaTopic.LogActionAccount, data={"message": json_mess}
    )


def push_message_kafka(topic: str, data: dict, key=None):
    key = key if key else topic
    KafkaProducerManager().flush_message(topic=topic, key=key, value=data)


def build_response_from_list(list_value):
    data = {}
    for item in list_value:
        data[item] = item
    return {"code": 200, "data": data}


def split_list(input_list, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(input_list), n):
        yield input_list[i: i + n]


@Singleton
class ConfigJWT:

    def __init__(self):
        self.config_anonymous = LRUCacheDict(expiration=3600)
        self.config_auth = LRUCacheDict(expiration=3600)
        self.config_basic = LRUCacheDict(expiration=900)

    def get_config_anonymous(self, merchant_id):
        from .call_api import CallAPI
        data = None
        try:
            try:
                data = self.config_anonymous.getitem(merchant_id)
            except:
                data = None
            if not data:
                data = CallAPI.get_config_jwt_anonymous(merchant_id)
                if data:
                    self.config_anonymous.set_item(merchant_id, data)
        except Exception as er:
            print("admin_sdk::get_config_anonymous: error: {}".format(er))
        return data

    def get_config_auth(self, merchant_id):
        data = None
        try:
            try:
                data = self.config_auth.getitem(merchant_id)
            except:
                data = None
            if not data:
                data = get_merchant_auth(merchant_id)
                if data:
                    self.config_auth.set_item(merchant_id, data)
        except Exception as er:
            print("admin_sdk::get_config_auth: error: {}".format(er))
        return data

    def get_config_basic(self, basic_key):
        data = None
        try:
            try:
                data = self.config_basic.getitem(basic_key)
            except:
                data = None
            if not data:
                if check_basic_auth_v2(basic_key):
                    data = "allow"
                    self.config_basic.set_item(basic_key, data)
                else:
                    data = "deny"
                    self.config_basic.set_item(basic_key, data)
        except Exception as er:
            print("admin_sdk::get_config_auth: error: {}".format(er))
        return data


def create_jwt_anonymous(merchant_id, data_jwt, session_time):
    if not merchant_id or not isinstance(merchant_id, str):
        raise ValueError("merchant_id not none")
    if not data_jwt or not isinstance(data_jwt, dict):
        raise ValueError("data_jwt not none")
    # if not isinstance(data_jwt.get("permissions"), dict):
    #     raise ValueError("permissions not valid")
    jwt_config = ConfigJWT().get_config_anonymous(merchant_id)
    if not jwt_config:
        raise ValueError("jwt config not none")
    algorithm = jwt_config.get("algorithm")
    secret_key = jwt_config.get("secret_key")
    exp = jwt_config.get("exp")
    if isinstance(session_time, int) and session_time > 0:
        exp = session_time
    time_start = time.time()
    data_jwt.update({
        "jwt_type": "anonymous",
        "exp": time_start + exp,
        "iat": time_start,
        "merchant_id": merchant_id,
    })
    encoded = jwt.encode(data_jwt, secret_key, algorithm=algorithm)
    return encoded
