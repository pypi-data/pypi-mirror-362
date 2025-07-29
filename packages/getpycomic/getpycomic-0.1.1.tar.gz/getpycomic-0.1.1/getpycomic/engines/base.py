# -*- coding: utf-8 -*-
"""
"""

from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):
    @abstractmethod
    def close(self) -> None:
        """
        """
        raise NotImplementedError()

    @abstractmethod
    def setup(self) -> None:
        """
        """
        raise NotImplementedError()

    @abstractmethod
    def search(self) -> None:
        """
        """
        raise NotImplementedError()

    @abstractmethod
    def wait_for_element(self) -> None:
        """
        """
        raise NotImplementedError()

    @abstractmethod
    def get_chapters(self) -> None:
        """
        """
        raise NotImplementedError()

    @abstractmethod
    def get_images(self) -> None:
        """
        """
        raise NotImplementedError()


    def __str__(self) -> str:
        """
        """
        return "Engine: %s" % (self.__class__.__name__)

    def __repr__(self) -> str:
        """
        """
        return "<[ %s ]>" % (self.__str__)
