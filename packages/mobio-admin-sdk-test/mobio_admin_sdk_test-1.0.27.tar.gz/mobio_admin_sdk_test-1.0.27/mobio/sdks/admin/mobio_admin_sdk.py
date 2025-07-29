from mobio.libs.Singleton import Singleton

# from mobio.libs.ciphers import MobioCrypt2
# from mobio.sdks.license import MobioLicenseSDK
from .aes_cipher import CryptUtil
from .config import Cache, SystemConfigKeys
from .device_utils import DeviceInfo
from .http_jwt_auth import HttpJwtAuth
from .mobio_authorization import MobioAuthorization


def sdk_pre_check(func):
    def decorated_function(*args, **kwargs):
        if not MobioAdminSDK().admin_host:
            raise ValueError("admin_host None")
        if not MobioAdminSDK().module_encrypt:
            raise ValueError("module_encrypt None")
        if not MobioAdminSDK().module_use:
            raise ValueError("module_use None")
        if MobioAdminSDK().admin_version not in MobioAdminSDK.LIST_VERSION_VALID:
            raise ValueError("admin_version invalid")
        # if not MobioAdminSDK().module_valid:
        #     raise ValueError("module invalid")

        return func(*args, **kwargs)

    return decorated_function


@Singleton
class MobioAdminSDK(object):
    DEFAULT_REQUEST_TIMEOUT_SECONDS = 15
    LIST_VERSION_VALID = ["v1.0", "api/v2.0", "api/v2.1"]

    def __init__(self):
        self.admin_host = ""
        self.admin_version = MobioAdminSDK.LIST_VERSION_VALID[-1]
        self.module_encrypt = ""
        self.module_use = ""
        self.request_header = None
        self.module_valid = False
        self.redis_connection = None

    @property
    def p_module_valid(self):
        return self.module_valid

    def config(
            self,
            admin_host=None,
            redis_uri=None,
            module_use=None,
            module_encrypt=None,
            api_admin_version=None,
    ):
        self.admin_host = SystemConfigKeys.ADMIN_HOST
        self.module_encrypt = module_encrypt
        self.module_use = module_use
        if api_admin_version:
            self.admin_version = api_admin_version
        if module_use:
            self.request_header = {"X-Module-Request": module_use, "X-Mobio-SDK": "ADMIN"}
        # if module_use and module_encrypt:
        #     # if module_use == MobioCrypt2.d1(module_encrypt, enc="utf-8"):
        #     #     self.module_valid = True
        #     # else:
        #     #     self.module_valid = False
        #     self.module_valid = True

        if SystemConfigKeys.vm_type and not CryptUtil().license_server_valid():
            raise ValueError("license server invalid")

        self.redis_connection = Cache().get_redis_connection()

        # MobioLicenseSDK().config(
        #     admin_host=admin_host,
        #     redis_uri=os.environ.get("REDIS_URI"),
        #     module_use=module_use,
        #     module_encrypt=module_encrypt,
        #     license_key=SystemConfigKeys.LICENSE_KEY,
        # )

    @staticmethod
    @sdk_pre_check
    def create_mobio_verify_token():
        MobioAuthorization().local_redis = MobioAdminSDK().redis_connection
        return HttpJwtAuth(MobioAuthorization())

    @staticmethod
    @sdk_pre_check
    def get_value_from_token(key, access_token=None):
        """
        :param key: is None return dict jwt
        :param access_token:
        :return:
        """
        if access_token:
            if key is None:
                return MobioAuthorization().jwt_decode_base64()
            return MobioAuthorization().get(access_token, key)
        else:
            return MobioAuthorization().get_jwt_value(key=key)

    @staticmethod
    @sdk_pre_check
    def request_get_merchant_config_host(
            merchant_id,
            key=None,
            admin_version=None,
            request_timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        from .call_api import CallAPI

        return CallAPI.get_merchant_config_host(
            merchant_id,
            key_host=key,
            admin_version=admin_version,
            request_timeout=request_timeout,
        )

    @staticmethod
    @sdk_pre_check
    def request_check_merchant_is_brand(
            merchant_id,
            admin_version=None,
            token_value=None,
            request_timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        from .call_api import CallAPI

        return CallAPI.get_info_merchant_brand_sub_brand(
            merchant_id,
            admin_version=admin_version,
            token_value=token_value,
            request_timeout=request_timeout,
        )

    @staticmethod
    @sdk_pre_check
    def request_get_info_staff(
            merchant_id,
            account_id,
            admin_version=None,
            token_value=None,
            request_timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        from .call_api import CallAPI

        return CallAPI.get_info_staff(
            merchant_id,
            account_id,
            admin_version=admin_version,
            token_value=token_value,
            request_timeout=request_timeout,
        )

    @staticmethod
    @sdk_pre_check
    def request_get_list_info_staff(
            merchant_id,
            params=None,
            admin_version=None,
            token_value=None,
            request_timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        from .call_api import CallAPI

        return CallAPI.get_list_info_staff(
            merchant_id,
            params=params,
            admin_version=admin_version,
            token_value=token_value,
            request_timeout=request_timeout,
        )

    @staticmethod
    @sdk_pre_check
    def request_get_list_parent_merchant(
            merchant_id,
            admin_version=None,
            token_value=None,
            request_timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        from .call_api import CallAPI

        return CallAPI.get_list_parent_merchant(
            merchant_id,
            admin_version=admin_version,
            token_value=token_value,
            request_timeout=request_timeout,
        )

    @staticmethod
    @sdk_pre_check
    def request_get_list_profile_group(
            merchant_id=None,
            params=None,
            admin_version=None,
            token_value=None,
            request_timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        from .call_api import CallAPI

        return CallAPI.get_list_profile_group(
            merchant_id=merchant_id,
            params=params,
            admin_version=admin_version,
            token_value=token_value,
            request_timeout=request_timeout,
        )

    @staticmethod
    @sdk_pre_check
    def request_get_list_sub_brand(
            params=None,
            admin_version=None,
            token_value=None,
            request_timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        from .call_api import CallAPI

        return CallAPI.get_list_subbrands(
            params=params,
            admin_version=admin_version,
            token_value=token_value,
            request_timeout=request_timeout,
        )

    @staticmethod
    @sdk_pre_check
    def request_get_info_sub_brand(
            subbrand_id=None,
            admin_version=None,
            token_value=None,
            request_timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        from .call_api import CallAPI

        return CallAPI.get_info_subbrand(
            subbrand_id=subbrand_id,
            admin_version=admin_version,
            token_value=token_value,
            request_timeout=request_timeout,
        )

    @staticmethod
    @sdk_pre_check
    def admin_save_log_action_account(json_mess):
        from .utils import push_kafka_log_action_account

        return push_kafka_log_action_account(json_mess)

    @staticmethod
    @sdk_pre_check
    def request_get_merchant_config_other(
            merchant_id=None,
            list_key=None,
            admin_version=None,
            request_timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
    ):
        from .call_api import CallAPI

        return CallAPI.get_merchant_config_other(
            merchant_id,
            list_key=list_key,
            admin_version=admin_version,
            request_timeout=request_timeout,
        )

    @staticmethod
    @sdk_pre_check
    def request_get_partner_info(
            partner_key=None,
            decrypt_data=False,
    ):
        from .utils import get_partner_info_decrypt
        return get_partner_info_decrypt(partner_key=partner_key, decrypt=decrypt_data)

    @staticmethod
    @sdk_pre_check
    def push_message_to_kafka(topic: str, data: dict, key=None):
        from .utils import push_message_kafka
        return push_message_kafka(topic, data, key)

    @staticmethod
    @sdk_pre_check
    def get_fields_config_encrypt(merchant_id, module):
        from .call_api import CallAPI
        return CallAPI.get_list_fields_config_encrypt(merchant_id, module)

    @staticmethod
    @sdk_pre_check
    def encrypt_values(merchant_id, module, field, values):
        from .encrypt_utils import EncryptFieldUtils
        return EncryptFieldUtils.encrypt_field_by_config(merchant_id, module, field, values)

    @staticmethod
    @sdk_pre_check
    def encrypt_values_object(merchant_id, module, field, values):
        from .encrypt_utils import EncryptFieldUtils
        return EncryptFieldUtils.encrypt_field_object_by_config(merchant_id, module, field, values)

    @staticmethod
    @sdk_pre_check
    def decrypt_values(merchant_id, module, field, values):
        from .encrypt_utils import EncryptFieldUtils
        return EncryptFieldUtils.decrypt_field_by_config(merchant_id, module, field, values)

    def redis_get_value(self, key_cache):
        return self.redis_connection.get(key_cache)

    def redis_set_value_expire(self, key_cache, value_cache, time_seconds=3600):
        self.redis_connection.setex(key_cache, time_seconds, value_cache)

    def redis_delete_key(self, key_cache):
        self.redis_connection.delete(key_cache)

    @staticmethod
    @sdk_pre_check
    def request_get_config_time_and_currency(merchant_id):
        from .date_utils import ConvertTime
        return ConvertTime.get_config_time_and_currency(merchant_id)

    @staticmethod
    @sdk_pre_check
    def convert_datetime_to_format(merchant_id: str, from_date, format_type: int, tz=None, lang=None):
        """
        :param merchant_id:
        :param from_date:
        :param format_type: FORMAT_ddmm = 1 FORMAT_ddmmYYYY = 2 FORMAT_ddmmYYYYHHMM = 3
        :param tz: number hour
        :param lang: vi en
        :return:
        """
        from .date_utils import ConvertTime
        return ConvertTime.convert_datetime_to_format(merchant_id, from_date, format_type, tz, lang)

    @staticmethod
    @sdk_pre_check
    def gen_jwt_anonymous_user(merchant_id: str, data_jwt: dict, session_time=None):
        from .utils import create_jwt_anonymous
        return create_jwt_anonymous(merchant_id, data_jwt, session_time)

    @staticmethod
    @sdk_pre_check
    def validate_token_jwt(token_jwt=None, verify_only_signature=False):
        return MobioAuthorization().verify_and_get_body_jwt(token_jwt, verify_signature=verify_only_signature)

    @staticmethod
    def detect_device_info(ua_string=None):
        return DeviceInfo(ua_string).get_device_info()

    @staticmethod
    def masking_value(value, use_format, format_logic, symbol_mas="*"):
        from .encrypt_utils import EncryptFieldUtils
        return EncryptFieldUtils.masking_value_by_config(
            value, format_logic, use_format=use_format, symbol_mas=symbol_mas)

    @staticmethod
    def masking_value_of_field(merchant_id, module, field, values, symbol_mas="*"):
        from .encrypt_utils import EncryptFieldUtils
        return EncryptFieldUtils.masking_value_field_by_config(
            merchant_id, module, field, values, symbol_mas=symbol_mas)
