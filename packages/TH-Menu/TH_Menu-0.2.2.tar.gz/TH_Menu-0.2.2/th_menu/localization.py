from typing import Union

class LocalizationContext:
    def __init__(self, locale: str = "en", fallback: str = "en"):
        self.locale = locale
        self.fallback = fallback

    def translate(self, value: Union[str, dict]):
        if isinstance(value, dict):
            return value.get(self.locale) or value.get(self.fallback) or next(iter(value.values()))
        return value
