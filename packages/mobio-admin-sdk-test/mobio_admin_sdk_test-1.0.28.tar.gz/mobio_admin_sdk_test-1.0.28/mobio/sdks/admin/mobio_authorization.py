#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Author: AnhNT
    Company: MobioVN
    Date created: 26/02/2021

"""
from .config import SystemConfigKeys
from .http_jwt_auth import ProjectAuthorization, TYPICALLY
from flask import json, request
from jose import jwt
from mobio.libs.Singleton import Singleton
# from mobio.sdks.license import MobioLicenseSDK
import re


@Singleton
class MobioAuthorization(ProjectAuthorization):
    def __init__(self):
        self.key = None
        self.algorithm = None
        self.options = {
            "verify_signature": True,
            "verify_aud": False,
            "verify_iat": False,
            "verify_exp": True,
            "verify_nbf": False,
            "verify_iss": False,
            "verify_sub": False,
            "verify_jti": False,
        }
        self.options_verify_signature = {
            "verify_signature": True,
            "verify_aud": False,
            "verify_iat": False,
            "verify_exp": False,
            "verify_nbf": False,
            "verify_iss": False,
            "verify_sub": False,
            "verify_jti": False,
        }
        self.local_redis = None

    @classmethod
    def __merchant_id__(cls, jwt_token=None):
        merchant_id = cls.get_value_from_decode_base64("merchant_id", jwt_token)
        if not merchant_id:
            merchant_id = request.headers.get(SystemConfigKeys.X_MERCHANT_ID, None)  # from Mobile
        if not merchant_id:
            print("admin_sdk:: __merchant_id__ None")
        return merchant_id

    @classmethod
    def get_value_from_decode_base64(cls, key, jwt_token):
        result = None
        if not key or not jwt_token:
            return result
        try:
            b_json = cls.jwt_decode_base64(jwt_token)
            result = b_json.get(key, None) if b_json else None
        except Exception as e:
            print("admin_sdk:: get_value_from_decode_base64 error: {}, jwt_token: {}".format(e, jwt_token))
        return result

    @staticmethod
    def jwt_decode_base64(jwt_token):
        result = None
        if not jwt_token:
            return result
        try:
            from .utils import Base64
            result = json.loads(Base64.decode(jwt_token.split(".")[1]))
        except Exception as e:
            print("admin_sdk:: jwt_decode_base64 error: {}, jwt_token: {}".format(e, jwt_token))
        return result

    @staticmethod
    def get_auth_info(merchant_id):
        from .utils import ConfigJWT

        auth_info = ConfigJWT().get_config_auth(merchant_id)
        return (
            auth_info[SystemConfigKeys.JWT_SECRET_KEY],
            auth_info[SystemConfigKeys.JWT_ALGORITHM],
        )

    @staticmethod
    def get_auth_anonymous(merchant_id):
        from .utils import ConfigJWT

        auth_info = ConfigJWT().get_config_anonymous(merchant_id)
        return (
            auth_info.get("secret_key"),
            auth_info.get("algorithm"),
        )

    @classmethod
    def get_jwt_info(cls):
        return cls.get_auth_info(cls.__merchant_id__())

    def get(self, token, field_name):
        """
        lấy thông tin theo tên trường từ Json Web Token
        :param token:
        :param field_name:
        :return:
        """
        return self.get_value_from_decode_base64(field_name, token)

    def _encode(self, body):
        try:
            return jwt.encode(body, self.key, self.algorithm)
        except Exception as e:
            print("admin_sdk::can not encode token: {} ; key: {}, algorithm: {}".format(
                str(e), self.key, self.algorithm))
            return None

    def _decode(self, body, secret_key=None, algorithm=None, options=None):
        if not secret_key or not algorithm:
            secret_key = self.key
            algorithm = self.algorithm
        if not options:
            options = self.options
        try:
            return jwt.decode(body, secret_key, algorithm, options)
        except Exception as e:
            print("admin_sdk::can not decode token: {} ; key: {}, algorithm: {}".format(
                str(e), secret_key, algorithm))
            return None

    def is_permitted(self, jwt_token, typically, method):
        """
        hàm kiểm tra method có được phân quyền hay không
        :param jwt_token:
        :param typically:
        :param method:
        :return:
        """
        return True

    def verify_token(self, jwt_token, typically):
        """
        nếu là module có chức năng au then thì kiem tra trong redis
        nếu là module khác thì gọi moddule authen để verify token
        :param typically:
        :param jwt_token:
        :return: trả về token nếu hợp lệ
        """
        try:
            # if MobioAuthorization.license_merchant_expire():
            #     return None

            if typically == TYPICALLY.BEARER or typically == TYPICALLY.DIGEST:
                body_jwt = self.verify_and_get_body_jwt(jwt_token)
                if not body_jwt:
                    return None
                arr_token = jwt_token.split(".")
                # kiểm tra token trong REDIS
                verify_token = arr_token[2]
                value = self.local_redis.get(verify_token)
                if not value:
                    print("admin_sdk::verify_token: {} not found in redis".format(verify_token))
                    return None
                return jwt_token

            elif typically == TYPICALLY.BASIC:
                from .utils import ConfigJWT
                if ConfigJWT().get_config_basic(jwt_token) != "allow":
                    print("admin_sdk:: {} basic key invalid".format(jwt_token))
                    return None
                    # if not MobioAuthorization.check_app_data_out(jwt_token):
                    #     raise ValueError("admin_sdk:: {} basic key invalid".format(jwt_token))
                return jwt_token

        except Exception as e:
            print("admin_sdk::MobioAuthorization::verify_token: ERROR: {}".format(e))
        return None
    
    def get_jwt_value(self, key=None):
        try:
            auth_type, token = self.get_token_from_header()
            if key is None:
                return self.jwt_decode_base64(token)
            return self.get(token, key)
        except Exception as err:
            print("admin_sdk::get_jwt_value err: {}, key: {}".format(err, key))
            return None

    # @staticmethod
    # def license_merchant_expire():
    #     from .utils import get_list_parent_merchant
    #     merchant_expire = True
    #     try:
    #         x_merchant_id = request.headers.get(SystemConfigKeys.X_MERCHANT_ID)
    #         if not x_merchant_id:
    #             print("admin_sdk::check_time_merchant_expire X-Merchant-ID not found")
    #         else:
    #             data_parent = get_list_parent_merchant(merchant_id=x_merchant_id,
    #                                                    token_value=SystemConfigKeys.MOBIO_TOKEN)
    #             if data_parent and data_parent.get("data") and len(data_parent.get("data")) > 0:
    #                 root_merchant_id = data_parent.get("data")[0].get("root_merchant_id")
    #                 if root_merchant_id:
    #                     merchant_expire = MobioLicenseSDK().merchant_has_expired(
    #                         root_merchant_id
    #                     )
    #                 else:
    #                     print("admin_sdk::check_time_merchant_expire root_merchant_id not found")
    #             else:
    #                 print("admin_sdk::check_time_merchant_expire parent merchant not found")
    #
    #     except Exception as e:
    #         print("admin_sdk::check_time_merchant_expire: ERROR: %s" % e)
    #     return merchant_expire

    @classmethod
    def check_anonymous_permissions(cls, jwt_token):
        # VD path: a = "/tag/api/v1.0/tags/(.*)/list"
        permissions = cls.get_value_from_decode_base64("permissions", jwt_token)
        if isinstance(permissions, dict):
            path_query = request.path
            method = request.method.lower()
            if permissions.get(path_query) and method in permissions.get(path_query):
                return True
            # check pattern neu co
            for k, v in permissions.items():
                pattern_path = re.compile(k)
                if bool(pattern_path.match(path_query)) and method in v:
                    return True
        return False

    @classmethod
    def get_token_from_header(cls):
        auth_type, jwt_token = request.headers["Authorization"].split(None, 1)
        return auth_type, jwt_token

    def verify_and_get_body_jwt(self, jwt_token=None, verify_signature=False):
        try:
            if not jwt_token:
                auth_type, jwt_token = self.get_token_from_header()
            b_json = self.jwt_decode_base64(jwt_token)
            if not b_json:
                return None
            jwt_type = b_json.get("jwt_type")
            merchant_id = b_json.get("merchant_id")
            if jwt_type == "anonymous":
                secret_key, algorithm = self.get_auth_anonymous(merchant_id)
            else:
                secret_key, algorithm = self.get_auth_info(merchant_id)
                self.key = secret_key
                self.algorithm = algorithm
            if verify_signature:
                verify_options = self.options_verify_signature
            else:
                verify_options = self.options
            body = self._decode(jwt_token, secret_key=secret_key, algorithm=algorithm, options=verify_options)
            return body
        except Exception as e:
            print("admin_sdk::verify_and_get_body_jwt: ERROR: {}".format(e))
        return None

    def verify_anonymous_signature(self, jwt_token, typically=None):
        """
        :param typically:
        :param jwt_token:
        :return: trả về token nếu hợp lệ
        """
        try:
            body_jwt = self.jwt_decode_base64(jwt_token)
            if not body_jwt:
                return None
            jwt_type = body_jwt.get("jwt_type")
            merchant_id = body_jwt.get("merchant_id")
            if jwt_type == "anonymous":
                secret_key, algorithm = self.get_auth_anonymous(merchant_id)
                body = self._decode(jwt_token, secret_key=secret_key, algorithm=algorithm,
                                    options=self.options_verify_signature)
                return body
        except Exception as e:
            print("admin_sdk::MobioAuthorization::verify_anonymous_signature: ERROR: {}".format(e))
        return None

    def verify_anonymous(self, jwt_token, typically=None):
        """
        :param typically:
        :param jwt_token:
        :return: trả về token nếu hợp lệ
        """
        try:
            body_jwt = self.jwt_decode_base64(jwt_token)
            if not body_jwt:
                return None
            jwt_type = body_jwt.get("jwt_type")
            merchant_id = body_jwt.get("merchant_id")
            if jwt_type == "anonymous":
                secret_key, algorithm = self.get_auth_anonymous(merchant_id)
                body = self._decode(jwt_token, secret_key=secret_key, algorithm=algorithm)
                return body
        except Exception as e:
            print("admin_sdk::MobioAuthorization::verify_anonymous: ERROR: {}".format(e))
        return None
