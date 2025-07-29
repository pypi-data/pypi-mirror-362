from .db import insert_url, get_url_by_code, get_url_by_long
from .config import BASE_DOMAIN
import string
import random

BASE62 = string.ascii_letters + string.digits

def generate_code(length=6):
    return ''.join(random.choices(BASE62, k=length))

def shorten_url(long_url):
    existing = get_url_by_long(long_url)
    if existing:
        return BASE_DOMAIN + existing[2]
    code = generate_code()
    insert_url(long_url, code)
    return BASE_DOMAIN + code

def expand_url(short_code):
    if short_code.startswith("http"):
        short_code = short_code.split("/")[-1]
    result = get_url_by_code(short_code)
    return result[1] if result else None