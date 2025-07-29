import datetime
import copy


class ConvertTime:
    FORMAT_ddmm = 1
    FORMAT_ddmmYYYY = 2
    FORMAT_ddmmYYYYHHMM = 3

    all_format = [FORMAT_ddmm, FORMAT_ddmmYYYY, FORMAT_ddmmYYYYHHMM]

    # TIME = 4
    # TIME_CUSTOM = 5
    # TIME_DELTA = 6

    @classmethod
    def convert_date_to_format(cls, time_in: datetime.datetime, convert_type=FORMAT_ddmm, lang="vi"):
        try:
            if time_in is not None and isinstance(time_in, datetime.datetime):
                # if time_zone is not None:
                #     time_in = add_timezone_to_date(time_in, time_zone)
                if convert_type == ConvertTime.FORMAT_ddmmYYYY:
                    return time_in.strftime("%d Thg %m, %Y") if lang == "vi" else time_in.strftime("%b %d, %Y")
                elif convert_type == ConvertTime.FORMAT_ddmmYYYYHHMM:
                    return time_in.strftime("%d Thg %m, %Y %H:%M") if lang == "vi" else (
                        time_in.strftime("%b %d, %Y %H:%M"))
                else:
                    return time_in.strftime("%d Thg %m") if lang == "vi" else time_in.strftime("%b %d")
            else:
                return None
        except:
            return None

    # @staticmethod
    # def convert_time(time_in: int, convert_type=TIME) -> str or None:
    #     try:
    #         if time_in is not None and isinstance(time_in, int):
    #             time_delta = timedelta(seconds=time_in)
    #             minutes, seconds = divmod(time_delta.seconds + time_delta.days * 86400, 60)
    #             hours, minutes = divmod(minutes, 60)
    #             if convert_type == ConvertTime.TIME_CUSTOM:
    #                 return "%sh %sm %ss" % (hours, minutes, seconds)
    #             elif convert_type == ConvertTime.TIME_DELTA:
    #                 return "%sd %sh %sm" % (time_delta.days, time_delta.seconds // 3600, minutes)
    #             else:
    #                 return "%s:%s:%s" % (hours, minutes, seconds)
    #     except:
    #         return None

    @classmethod
    def get_utc_now(cls):
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        return now

    @classmethod
    def convert_date_to_timestamp(cls, vNgayThang):
        try:
            if vNgayThang is not None:
                return round(vNgayThang.replace(tzinfo=datetime.timezone.utc).timestamp())
            else:
                return None
        except:
            return None

    @classmethod
    def convert_timestamp_to_date_utc(cls, timestamp):
        try:
            if timestamp is not None:
                return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).replace(
                    tzinfo=datetime.timezone.utc
                )
            else:
                return None
        except:
            return None

    @classmethod
    def get_timestamp_utc_now(cls):
        return round(cls.get_utc_now().timestamp())

    @classmethod
    def add_timezone_to_date(cls, date_in: datetime.datetime, time_zone: int or float):
        return date_in + datetime.timedelta(hours=time_zone)

    @classmethod
    def convert_datetime_to_format(cls, merchant_id: str, from_date: datetime.datetime,
                                   format_type=FORMAT_ddmmYYYY, tz=None, lang=None):
        from .call_api import CallAPI
        if format_type not in cls.all_format:
            raise ValueError("format type not defind")
        date_input = copy.deepcopy(from_date)
        if tz is not None:
            date_input = cls.add_timezone_to_date(date_input, tz)
        if lang is None:
            lang = 'vi'
            list_field = ["lang_default"]
            data = CallAPI.get_merchant_config_other(merchant_id, list_field)
            if data and data.get("lang_default"):
                lang = data.get("lang_default")
        return cls.convert_date_to_format(time_in=date_input, convert_type=format_type, lang=lang)

    @classmethod
    def get_config_time_and_currency(cls, merchant_id):
        data_config = {
            "config_time": {
                "timezone": 7,
                "text": "(UTC+07:00) Bangkok, Hanoi, Jakarta",
                "location": "Asia/Saigon",
            },
            "currency_code": "vnd",
            "lang_default": "vi",
        }
        data = cls.get_config_merchant_for_fields(merchant_id)
        if data:
            if data.get("config_time"):
                data_config.update({"config_time": data.get("config_time")})
            if data.get("currency_code"):
                data_config.update({"currency_code": data.get("currency_code")})
            if data.get("lang_default"):
                data_config.update({"lang_default": data.get("lang_default")})
        return data_config

    @staticmethod
    def get_config_merchant_for_fields(merchant_id):
        from .call_api import CallAPI
        list_field = ["config_time", "currency_code", "lang_default"]
        return CallAPI.get_merchant_config_other(merchant_id, list_field)
