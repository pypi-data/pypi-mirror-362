import requests
import socket

class RouterHK:
    VERSION = '250715'
    BASE_URL = "https://router.hk/api"
    DEFAULT_TIMEOUT = 3
    ip_version = None
    api_status = None
    api_response = None
    api_error = None
    ip_address = None
    via_proxy_ip_address = None
    client_user_agent = None
    client_accept_language = None
    api_time_human_readable = None
    api_time = None

    def __init__(self):
        self.headers = {
            'User-Agent': f"{self.__class__.__name__}/{self.VERSION}",
        }

    def get(self, endpoint, params=None):
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            if self.ip_version == 4:
                socket.setdefaultfamily(socket.AF_INET)
            elif self.ip_version == 6:
                socket.setdefaultfamily(socket.AF_INET6)
            response = requests.get(url, params=params, timeout=self.DEFAULT_TIMEOUT, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            self.api_status = response.status_code
            self.api_response = response.json()
            return True
        except requests.exceptions.HTTPError as http_err:
            self.api_status = http_err.response.status_code
            self.api_error = http_err
            self.api_response = None
            self.api_time_human_readable = None
            self.api_time = None
            return False
        except Exception as err:
            print(f"An error occurred: {err}")  # Handle other errors

    def get_ip(self):
        if self.get('ip'):
            self.ip_address = self.api_response['ip_addr']
            self.via_proxy_ip_address = self.api_response['via_proxy_ip_addr']
            self.client_user_agent = self.api_response['user_agent']
            self.client_accept_language = self.api_response['accept_language']
            self.api_time_human_readable = self.api_response['time_human_readable']
            self.api_time = self.api_response['time']
            return self.ip_address
        else:
            self.ip_address = None
            self.via_proxy_ip_address = None
            self.client_user_agent = None
            self.client_accept_language = None
            return None
