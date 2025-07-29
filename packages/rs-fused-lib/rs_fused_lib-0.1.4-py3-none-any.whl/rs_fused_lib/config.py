# rs_fused_lib/config.py
BASE_URL = "http://10.1.113.136:18002/api"

def set_base_url(url: str):
    global BASE_URL
    BASE_URL = url

def get_base_url() -> str:
    return BASE_URL 