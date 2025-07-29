# -*- coding: utf-8 -*-
"""
"""

from getpycomic.pathclass import PathClass
from getpycomic.jsondata import JSONData

from getpycomic.models import Comic

from typing import TypeVar


Controller = TypeVar('Controller')


class Status:

    json = "data.json"

    def __init__(
        self,
        controller: Controller,
        base_path: str,
        language: str,
    ) -> None:
        """
        """
        self.language = language
        self.method = None  # str
        self.error = False  # bool

        self.controller = controller


        self.comic_name = None  # str
        self.chapter_id = None  # float
        self.imagechapter_id = None  # int

        self.last_chapter = None  # float



        self.base_path = base_path


        self.path_data_json = PathClass.join(
                                            self.base_path,
                                            Status.json
                                        )


    def clear(self) -> None:
        """
        """
        self.method = None
        self.error = False

    def check(self) -> None:
        """
        """
        self.to_load()

        if self.method is True:
            self.method
            self.error

    def to_dict(self) -> dict:
        """
        """
        if self.controller.get_current_comic is not None:
            comic_data = self.controller.get_current_comic.to_dict()
        else:
            comic_data = self.controller.get_current_comic

        return {
            "method": self.method,
            "error": self.error,
            "show": self.controller.show,
            "setup": self.controller.setup,

            "comic": comic_data,
            "comic_name": self.comic_name,
            "chapter_id": self.chapter_id,
            "imagechapter_id": self.imagechapter_id,
            "last_chapter": self.last_chapter,
        }

    def to_json(self) -> None:
        """
        """
        JSONData.to_save(
                    file_path=self.path_data_json,
                    data=self.to_dict()
                )


    def to_load(self) -> None:
        """
        """
        print("> to_load")
        data = JSONData.to_load(file_path=self.path_data_json)

        # print(data.keys())

        if data != {}:
            if data["comic"] is not None:
                comic_data = Comic.from_dict(data["comic"])
            else:
                comic_data = data["comic"]

            self.method = data["method"]
            self.error = data["error"]
            self.controller.show = data["show"]
            self.controller.setup = data["setup"]

            self.controller.current_comic = comic_data

            self.comic_name = data["comic_name"]
            self.chapter_id = data["chapter_id"]
            self.imagechapter_id = data["imagechapter_id"]

            self.last_chapter = data["last_chapter"]
