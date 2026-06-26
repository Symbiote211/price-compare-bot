import requests
from typing import Optional

def fetch(url: str, headers: dict = None, params: dict = None, timeout: int = 5) -> Optional[requests.Response]:
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9",
    }
    if headers:
        default_headers.update(headers)
    try:
        resp = requests.get(url, headers=default_headers, params=params, timeout=timeout, verify=False)
        return resp
    except Exception:
        return None
