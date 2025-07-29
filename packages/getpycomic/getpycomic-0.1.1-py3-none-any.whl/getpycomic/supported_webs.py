# -*- coding: utf-8 -*-
"""
"""


from getpycomic.pages import (
    TmoManga,
    ZonaTmo,
    NovelCool,

)


class Supported_Webs:
    tmomanga = TmoManga
    zonatmo = ZonaTmo
    novelcool = NovelCool
    # other websites in the future

    @classmethod
    def get_web(cls, key: str):
        return getattr(cls, key, "tmomanga")

    @classmethod
    def get_keys(cls):
        """
        """
        return [
            key for key, value in cls.__dict__.items()
            if callable(value)
            and not key.startswith("__")
            and key != "get_keys" and key != "get_web"
        ]
