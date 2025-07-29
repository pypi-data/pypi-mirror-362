# -*- coding: utf-8 -*-
"""
"""

import io

from typing import (
                    List,
                    Union,
                    TypeVar
                )



ImageChapter = TypeVar("ImageChapter")
Chapter = TypeVar("Chapter")
Volume = TypeVar("Volume")
Comic = TypeVar("Comic")


class ImageChapter:
    """
    """

    def __init__(
        self,
        id: int,
        name: str,
        extension: str,
        link: str,
        path: str = None,
    ) -> None:
        """
        """
        self.id = id
        self.name = name
        self.extension = extension
        self.link = link
        self.path = path

    def get_name(self) -> str:
        """
        """
        return "%03d%s" % (self.id, self.extension)

    def to_dict(self) -> dict:
        """
        """
        return {
            "id": self.id,
            "name": self.name,
            "extension": self.extension,
            "link": self.link,
            "path": self.path
        }

    @staticmethod
    def from_dict(data) -> ImageChapter:
        """
        """
        return ImageChapter(
            id=data["id"],
            name=data["name"],
            extension=data["extension"],
            link=data["link"],
            path=data.get("path")
        )

    def __str__(self) -> str:
        """
        """
        return "<[ Image: %s ]>" % (self.get_name())

    def __repr__(self) -> str:
        """
        """
        return self.__str__()


class Chapter:
    """
    """

    def __init__(
        self,
        id: float,
        name: str,
        link: str,
        images: List[ImageChapter] = [],
        path: str = None
    ) -> None:
        """
        """
        self.id = float(id)
        self.name = name
        self.link = link
        self.images = images
        self.path = path

    def amount_images(self) -> int:
        """
        """
        return len(self.images)

    @property
    def get_id(self) -> str:
        """
        """
        return "%.2f" % self.id

    def to_dict(self) -> dict:
        """
        """
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "images": [img.to_dict() for img in self.images],
            "path": self.path
        }

    @staticmethod
    def from_dict(data) -> Chapter:
        """
        """
        return Chapter(
            id=data["id"],
            name=data["name"],
            link=data["link"],
            images=[ImageChapter.from_dict(i) for i in data.get("images", [])],
            path=data.get("path")
        )

    def __lt__(self, obj):
        """
        """
        return self.id < obj.id

    def __str__(self) -> str:
        """
        """
        return "<[ Chapter: %s, Images: %i ]>" % (
                            self.name,
                            len(self.images)
                        )
    def __repr__(self) -> str:
        """
        """
        return self.__str__()


class Volume:
    """
    """

    def __init__(
        self,
        volume: int,
        list_chapters: List[Chapter]
    ) -> None:
        """
        """
        self.volume = volume
        self.list_chapters = list_chapters
        self.n_chapters = 0

    def add(
        self,
        chapter: Chapter
    ) -> None:
        """
        """
        self.list_chapters.append(chapter)
        self.n_chapters += 1

    def get_range_chapters(
        self
    ) -> str:
        """
        """
        return "%.1f-%.1f" % (
                            self.list_chapters[0].id,
                            self.list_chapters[-1].id
                        )

    def to_dict(self) -> dict:
        """
        """
        return {
            "volume": self.volume,
            "list_chapters": [c.to_dict() for c in self.list_chapters]
        }

    @staticmethod
    def from_dict(data) -> Volume:
        """
        """
        return Volume(
            volume=data["volume"],
            list_chapters=[Chapter.from_dict(c) for c in data["list_chapters"]]
        )

    def __str__(self) -> str:
        """
        """
        return "<[ Volume: %d, Chapters: %d ]>" % (
                                                self.volume,
                                                self.n_chapters
                                            )

    def __repr__(self) -> str:
        """
        """
        return self.__str__()


class Comic:
    """
    """

    def __init__(
        self,
        name: str = None,
        original_name: str = None,
        link: str = None,
        chapters: List[Chapter] = [],
        path: str = None,
        volumes: dict = None
    ) -> None:
        """
        """
        self.name = name
        self.original_name = original_name
        self.link = link
        self.chapters = chapters
        self.path = path
        self.volumes = volumes

    def to_dict(self) -> dict:
        """
        """
        return {
            "name": self.name,
            "link": self.link,
            "chapters": [ch.to_dict() for ch in self.chapters],
            "path": self.path,
            "volumes": {k: v.to_dict() for k, v in self.volumes.items()} if self.volumes else None
        }

    @staticmethod
    def from_dict(data) -> Comic:
        """
        """
        return Comic(
            name=data["name"],
            link=data["link"],
            chapters=[Chapter.from_dict(ch) for ch in data.get("chapters", [])],
            path=data.get("path"),
            volumes={int(k): Volume.from_dict(v) for k, v in data.get("volumes", {}).items()} if data.get("volumes") else None
        )

    def __str__(self) -> str:
        """
        """
        return '<[ Name: %s, Chapters: %i ]>' % (
                            self.name,
                            len(self.chapters)
                        )

    def __repr__(self) -> str:
        """
        """
        return self.__str__()
