import os
import json

locale_strings = {}

def load_strings(locale_name: str):
    global locale_strings
    if locale_name in ['en', 'ru']:
        with open(os.path.join(os.path.dirname(__file__), '../locale/', locale_name + '.json')) as f:
            locale_strings = json.load(f)

def load_system_locale():
    if os.getenv('LANG').startswith('ru_'):
        load_strings('ru')
    else:
        load_strings('en')

def i18n_get(key: str) -> str:
    if key in locale_strings:
        return locale_strings[key]
    else:
        return key

load_system_locale()