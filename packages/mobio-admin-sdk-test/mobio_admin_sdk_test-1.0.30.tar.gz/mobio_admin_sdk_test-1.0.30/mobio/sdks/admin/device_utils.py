from user_agents import parse as ua_parse
from flask import request


class DeviceInfo:
    def __init__(self, ua_string=None):
        self.ua_string = ua_string

    @staticmethod
    def get_ip_address():
        try:
            header_data = request.headers
            current_ip = request.remote_addr
            if header_data.get("X-Real-Ip"):
                current_ip = header_data.get("X-Real-Ip")
            return current_ip
        except:
            return ""

    def parse_user_agent_info(self):
        try:
            if not self.ua_string:
                header_data = request.headers
                self.ua_string = header_data.get('User-Agent')
            device_parse = ua_parse(self.ua_string)
            device_info = {
                "device_os": device_parse.os.family,
            }
            return device_info
        except:
            return {}

    def get_device_info(self):
        device_info = {}
        user_agent_info = self.parse_user_agent_info()
        device_info.update(user_agent_info)
        device_info.update({"ip_address": self.get_ip_address()})
        return device_info

