import requests
from .aes_cipher import CryptUtil
from .config import (
    SystemConfigKeys, UrlConfig, lru_redis_cache, RedisKeyCache, CodeErrorEncrypt
)
from .mobio_admin_sdk import MobioAdminSDK
from flask import request


class CallAPI:

    @staticmethod
    @lru_redis_cache.add()
    def get_list_fields_config_encrypt(merchant_id, module):
        api_version = MobioAdminSDK().admin_version
        adm_url = str(UrlConfig.GET_LIST_FIELD_CONFIG_ENCRYPT).format(
            host=MobioAdminSDK().admin_host, version=api_version
        )
        params = {"module": module}
        request_header = {
            "Authorization": SystemConfigKeys.MOBIO_TOKEN,
            "X-Merchant-Id": merchant_id
        }
        if MobioAdminSDK().request_header:
            request_header.update(MobioAdminSDK().request_header)
        response = requests.get(
            adm_url,
            params=params,
            headers=request_header,
            timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        result = response.json()
        if result and result.get("data"):
            return result.get("data")
        else:
            return []

    @staticmethod
    def kms_viettel_get_token(kms_id):
        try:
            key_cache = RedisKeyCache.kms_viettel_get_token.format(kms_id)
            token_key = MobioAdminSDK().redis_get_value(key_cache)
            if token_key:
                return token_key.decode('utf-8')
            else:
                api_version = MobioAdminSDK().admin_version
                adm_url = str(UrlConfig.GET_TOKEN_KMS_CONFIG).format(
                    host=MobioAdminSDK().admin_host, version=api_version
                )
                params = {"kms_id": kms_id}
                request_header = {
                    "Authorization": SystemConfigKeys.MOBIO_TOKEN,
                }
                if MobioAdminSDK().request_header:
                    request_header.update(MobioAdminSDK().request_header)
                response = requests.get(
                    adm_url,
                    params=params,
                    headers=request_header,
                    timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
                )
                response.raise_for_status()
                result = response.json()
                if result and result.get("data"):
                    token_key = result.get("data").get("access_token")
                    expires_in = int(result.get("data").get("expires_in"))
                    expires_in = expires_in - 30 if expires_in > 30 else expires_in
                    MobioAdminSDK().redis_set_value_expire(key_cache, token_key, time_seconds=expires_in)
                    return token_key
        except Exception as er:
            print("admin_sdk::kms_viettel_get_token: error: {}".format(er))
        return None

    @classmethod
    def request_kms_viettel_encrypt(cls, kms_info, access_token, list_data):
        data_result = {
            "data": {}, "data_error": {}
        }
        try:
            kms_enc = kms_info.get("kms_enc")
            api_url = kms_enc.get("api_url")
            request_header = {
                "Authorization": "Bearer {}".format(access_token),
                "Content-Type": "application/json"
            }
            body_request = {
                "msisdns": list_data
            }
            response = requests.post(
                api_url,
                headers=request_header,
                json=body_request,
                timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS
            )
            response.raise_for_status()
            result = response.json()
            print("admin_sdk:: encrypt status: {}, text: {}".format(response.status_code, result))
            if result.get("content"):
                for item in result.get("content"):
                    if item.get("value"):
                        data_result["data"][item.get("key")] = item.get("value")
                    else:
                        data_result["data_error"][item.get("key")] = CodeErrorEncrypt.encrypt_api_error
                return data_result
            data_result["data_error"] = cls.build_data_error_by_code(list_data, CodeErrorEncrypt.encrypt_api_error)
        except Exception as er:
            print("admin_sdk::request_kms_viettel_encrypt: error: {}".format(er))
            data_result["data_error"] = cls.build_data_error_by_code(list_data, CodeErrorEncrypt.encrypt_api_timeout)
        return data_result

    @classmethod
    def request_kms_viettel_decrypt(cls, kms_info, access_token, list_data):
        data_result = {
            "data": {}, "data_error": {}
        }
        try:
            kms_dec = kms_info.get("kms_dec")
            api_url = kms_dec.get("api_url")
            request_header = {
                "Authorization": "Bearer {}".format(access_token),
                "Content-Type": "application/json"
            }
            body_request = {
                "msisdns": list_data
            }
            response = requests.post(
                api_url,
                headers=request_header,
                json=body_request,
                timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS
            )
            response.raise_for_status()
            result = response.json()
            print("admin_sdk:: decrypt status: {}, text: {}".format(response.status_code, result))
            if result.get("content"):
                for item in result.get("content"):
                    if item.get("value"):
                        data_result["data"][item.get("key")] = item.get("value")
                    else:
                        data_result["data_error"][item.get("key")] = CodeErrorEncrypt.encrypt_api_error
                return data_result
            data_result["data_error"] = cls.build_data_error_by_code(list_data, CodeErrorEncrypt.encrypt_api_error)
        except Exception as er:
            print("admin_sdk::request_kms_viettel_encrypt: error: {}".format(er))
            data_result["data_error"] = cls.build_data_error_by_code(list_data, CodeErrorEncrypt.encrypt_api_timeout)
        return data_result

    @staticmethod
    def build_data_error_by_code(list_data, error_code):
        data_error = {}
        for item in list_data:
            data_error[item] = error_code
        return data_error

    @staticmethod
    @lru_redis_cache.add()
    def get_merchant_config_other(
            merchant_id,
            list_key=None,
            admin_version=None,
            request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        api_version = MobioAdminSDK().admin_version
        if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
            api_version = admin_version
        adm_url = str(UrlConfig.GET_DETAIL_MERCHANT_CONFIG).format(
            host=MobioAdminSDK().admin_host,
            version=api_version,
            merchant_id=merchant_id,
        )
        request_header = {}
        if MobioAdminSDK().request_header:
            request_header.update(MobioAdminSDK().request_header)
        param = None
        if list_key and isinstance(list_key, list):
            param = {"fields": ",".join(list_key)}
        response = requests.get(
            adm_url,
            params=param,
            headers=request_header,
            timeout=request_timeout,
        )
        # response.raise_for_status()
        result = response.json()
        data = result.get("data", {}) if result and result.get("data", {}) else {}
        return data

    @staticmethod
    @lru_redis_cache.add()
    def get_merchant_config_host(
            merchant_id,
            key_host=None,
            admin_version=None,
            request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        if SystemConfigKeys.vm_type and not CryptUtil().license_server_valid():
            raise ValueError("license server invalid")

        api_version = MobioAdminSDK().admin_version
        if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
            api_version = admin_version
        adm_url = str(UrlConfig.GET_DETAIL_MERCHANT_CONFIG).format(
            host=MobioAdminSDK().admin_host,
            version=api_version,
            merchant_id=merchant_id,
        )
        request_header = {}
        if MobioAdminSDK().request_header:
            request_header.update(MobioAdminSDK().request_header)
        param = {"fields": ",".join(["internal_host", "module_host", "public_host", "config_host"])}
        response = requests.get(
            adm_url,
            params=param,
            headers=request_header,
            timeout=request_timeout,
        )
        response.raise_for_status()
        result = response.json()
        data = result.get("data", {}) if result and result.get("data", {}) else {}
        if key_host:
            return data.get(key_host)
        return data

    @staticmethod
    @lru_redis_cache.add()
    def get_info_merchant_brand_sub_brand(
            merchant_id,
            admin_version=None,
            token_value=None,
            request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        api_version = MobioAdminSDK().admin_version
        if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
            api_version = admin_version
        adm_url = str(UrlConfig.MERCHANT_RELATED).format(
            host=MobioAdminSDK().admin_host,
            version=api_version,
            merchant_id=merchant_id,
        )
        if token_value:
            request_header = {"Authorization": token_value}
        else:
            request_header = {"Authorization": request.headers.get("Authorization")}

        if MobioAdminSDK().request_header:
            request_header.update(MobioAdminSDK().request_header)
        response = requests.get(
            adm_url,
            headers=request_header,
            timeout=request_timeout,
        )
        response.raise_for_status()
        result = response.json()
        return result

    @staticmethod
    @lru_redis_cache.add()
    def get_info_staff(
            merchant_id,
            account_id,
            admin_version=None,
            token_value=None,
            request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        api_version = MobioAdminSDK().admin_version
        if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
            api_version = admin_version
        adm_url = str(UrlConfig.STAFF_INFO).format(
            host=MobioAdminSDK().admin_host,
            version=api_version,
            merchant_id=merchant_id,
            account_id=account_id,
        )
        if token_value:
            request_header = {"Authorization": token_value}
        else:
            request_header = {"Authorization": request.headers.get("Authorization")}
        if MobioAdminSDK().request_header:
            request_header.update(MobioAdminSDK().request_header)
        response = requests.get(
            adm_url,
            headers=request_header,
            timeout=request_timeout,
        )
        response.raise_for_status()
        result = response.json()
        return result

    @staticmethod
    @lru_redis_cache.add()
    def get_list_info_staff(
            merchant_id,
            params=None,
            admin_version=None,
            token_value=None,
            request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        api_version = MobioAdminSDK().admin_version
        if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
            api_version = admin_version
        adm_url = str(UrlConfig.LIST_STAFF_INFO).format(
            host=MobioAdminSDK().admin_host,
            version=api_version,
            merchant_id=merchant_id,
        )
        if token_value:
            request_header = {"Authorization": token_value}
        else:
            request_header = {"Authorization": request.headers.get("Authorization")}
        if MobioAdminSDK().request_header:
            request_header.update(MobioAdminSDK().request_header)
        response = requests.get(
            adm_url,
            params=params,
            headers=request_header,
            timeout=request_timeout,
        )
        response.raise_for_status()
        result = response.json()
        return result

    @staticmethod
    @lru_redis_cache.add()
    def get_list_parent_merchant(
            merchant_id,
            admin_version=None,
            token_value=None,
            request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        api_version = MobioAdminSDK().admin_version
        if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
            api_version = admin_version
        adm_url = str(UrlConfig.MERCHANT_PARENT).format(
            host=MobioAdminSDK().admin_host,
            version=api_version,
            merchant_id=merchant_id,
        )
        if token_value:
            request_header = {"Authorization": token_value}
        else:
            request_header = {"Authorization": request.headers.get("Authorization")}
        if MobioAdminSDK().request_header:
            request_header.update(MobioAdminSDK().request_header)
        response = requests.get(
            adm_url,
            headers=request_header,
            timeout=request_timeout,
        )
        response.raise_for_status()
        result = response.json()
        return result

    @staticmethod
    @lru_redis_cache.add()
    def get_list_profile_group(
            merchant_id=None,
            params=None,
            admin_version=None,
            token_value=None,
            request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        api_version = MobioAdminSDK().admin_version
        if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
            api_version = admin_version
        adm_url = str(UrlConfig.LIST_PROFILE_GROUP).format(
            host=MobioAdminSDK().admin_host, version=api_version
        )
        if token_value:
            request_header = {"Authorization": token_value}
        else:
            request_header = {"Authorization": request.headers.get("Authorization")}
        if merchant_id:
            request_header["X-Merchant-Id"] = merchant_id
        if MobioAdminSDK().request_header:
            request_header.update(MobioAdminSDK().request_header)
        response = requests.get(
            adm_url,
            params=params,
            headers=request_header,
            timeout=request_timeout,
        )
        response.raise_for_status()
        result = response.json()
        return result

    @staticmethod
    @lru_redis_cache.add()
    def get_list_subbrands(
            params=None,
            admin_version=None,
            token_value=None,
            request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        api_version = MobioAdminSDK().admin_version
        if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
            api_version = admin_version
        adm_url = str(UrlConfig.LIST_SUBBRANDS_BY_MERCHANT).format(
            host=MobioAdminSDK().admin_host, version=api_version
        )
        if token_value:
            request_header = {"Authorization": token_value}
        else:
            request_header = {"Authorization": request.headers.get("Authorization")}
        if MobioAdminSDK().request_header:
            request_header.update(MobioAdminSDK().request_header)
        response = requests.get(
            adm_url,
            params=params,
            headers=request_header,
            timeout=request_timeout,
        )
        response.raise_for_status()
        result = response.json()
        return result

    @staticmethod
    @lru_redis_cache.add()
    def get_info_subbrand(
            subbrand_id=None,
            admin_version=None,
            token_value=None,
            request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        api_version = MobioAdminSDK().admin_version
        if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
            api_version = admin_version
        adm_url = str(UrlConfig.GET_INFO_SUBBRAND).format(
            host=MobioAdminSDK().admin_host, version=api_version, subbrand_id=subbrand_id
        )
        if token_value:
            request_header = {"Authorization": token_value}
        else:
            request_header = {"Authorization": request.headers.get("Authorization")}

        if MobioAdminSDK().request_header:
            request_header.update(MobioAdminSDK().request_header)
        response = requests.get(
            adm_url,
            headers=request_header,
            timeout=request_timeout,
        )
        response.raise_for_status()
        result = response.json()
        return result

    @staticmethod
    @lru_redis_cache.add()
    def get_config_jwt_anonymous(merchant_id):
        """
        :param merchant_id:
        :return:  {
                "algorithm": algorithm,
                "secret_key": secret_key,
                "exp": expire_time,
            }
        """
        try:
            api_version = MobioAdminSDK().admin_version
            adm_url = str(UrlConfig.GET_CONFIG_JWT_ANONYMOUS).format(
                host=MobioAdminSDK().admin_host, version=api_version
            )
            request_header = {
                "Authorization": SystemConfigKeys.MOBIO_TOKEN,
                "X-Merchant-Id": merchant_id
            }
            if MobioAdminSDK().request_header:
                request_header.update(MobioAdminSDK().request_header)
            response = requests.get(
                adm_url,
                headers=request_header,
                timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            result = response.json()
            if result and result.get("data"):
                return result.get("data")
            else:
                return {}
        except Exception as er:
            print("admin_sdk::get_config_jwt_anonymous: error: {}".format(er))
            return {}
