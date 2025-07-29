# -*- coding: utf-8 -*-
"""
"""

class BaseMeta(type):

    def __str__(cls) -> str:
        """
        """
        return "<[ %s ]>" % (cls.base)

    def __repr__(cls) -> str:
        """
        """
        return "<[ %s ]>" % (cls.base)
