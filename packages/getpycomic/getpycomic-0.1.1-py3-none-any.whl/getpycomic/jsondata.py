# -*- coding: utf-8 -*-
"""
"""

import json

from typing import TypeVar, Union


Comic = TypeVar("Comic")


class JSONData:
    """
    """
    @staticmethod
    def to_save(
        file_path: str,
        data: dict
    ) -> None:
        """
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def to_load(
        file_path: str
    ) -> dict:
        """
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError as e:
            return {}
