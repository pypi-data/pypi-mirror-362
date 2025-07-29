# -*- coding: utf-8 -*-
"""
"""

from typing import (
        List,
        Union
    )

from getpycomic.models import (
        Comic,
        Chapter,
        Volume
    )


class VolumesSorter:
    """
    """
    CHAPTERS_BY_VOLUME = 6

    def __init__(self):
        """
        """
        self.volumes = {}
        self.chapters_in_volume = []
        self.chapters_wo_volume = {}

    def clear(self) -> None:
        """
        Clears attributes.
        """
        self.volumes = {}
        self.chapters_in_volume = []
        self.chapters_wo_volume = {}

    def __sequence_check(
        self,
        matrix: dict
    ) -> bool:
        """
        Checks the sequence of volumes and chapter ranges indicated by the user.

        Args
            matrix: dicctionary with volumes and chapters indicators.

        Returns
            bool: `True` or `False` if sequential or not.
        """
        # checks if keys is a int.
        if all([isinstance(i, int) for i in matrix.keys()]) is False:
            return False

        # checks if `keys` is a sequence
        seq_keys = list(matrix.keys())
        # print(seq_keys)
        min_ = min(list(matrix.keys()))
        max_ = max(list(matrix.keys()))
        if seq_keys != [i for i in range(min_, max_ + 1)]:
            return False

        # checks if `values` is a sequence
        seq_values = [
                    int(x) for i in matrix.values()
                    if i != ""
                    for x in (i.split("-") if isinstance(i, str) else i)
                ]

        seq_values = []
        for val in matrix.values():
            if not val:
                continue
            if isinstance(val, str):
                values = val.split("-")
            if isinstance(val, (list, tuple)):
                values = val
            seq_values.extend(int(i) for i in values)

        if sorted(seq_values) != seq_values:
            return False

        return True

    def sorter(
        self,
        comicObj: Comic = None,
        volumes_dict_chapters: dict = None,
        chapters_by_volume: int = None,
    ) -> dict:
        """
        Sorts chapters by volume follow the indication given by user.

        In two formats:
            * volumes_dict_chapters={volume_int: "start-end"}
            * volumes_dict_chapters={volume_int: [star, end]}

        *volume_int* must be an integer.
        *start* and *end* must be integers or a string of an integer.

        If the volume is not indicated, all chapters will be stored in a single
        volume.
        If the volume is specified, but not the chapter indicators, the
        remaining chapters will be stored in a single volume.

        Args
            comicObj: `Comic` instance with chapters of comic.
            volumes_dict_chapters: dicctionary with order of volumes and
                                   chapters.
            chapters_by_volume: int, number of chapters by volume.

        Returns
            dict: dicctionary with volumes and chapters.
            None: if dicctionary given not is correct.
        """
        self.clear()

        # print("> " , volumes_dict_chapters, chapters_by_volume)

        # print(comicObj, chapters_by_volume)
        if comicObj is None or isinstance(comicObj, Comic) is False:
            return {}

        # if volumes_dict_chapters is None
        if volumes_dict_chapters is None or len(volumes_dict_chapters) == 0:
            volumes_dict_chapters = {}
            volume_ = 1
            n_chaps = len(comicObj.chapters)

            if chapters_by_volume is not None:
                chapters_by_volume = chapters_by_volume
            else:
                chapters_by_volume = VolumesSorter.CHAPTERS_BY_VOLUME

            for i in range(0, n_chaps, chapters_by_volume):
                chunk = comicObj.chapters[0 + i: chapters_by_volume + i]
                chap_ids = [i.id for i in chunk]
                volumes_dict_chapters[volume_] = [min(chap_ids), max(chap_ids)]
                volume_ += 1

        # print(volumes_dict_chapters)

        check = self.__sequence_check(matrix=volumes_dict_chapters)
        # print(">> ", check, chapters_by_volume)
        if check is False:
            return {}

        try:
            for k, v in volumes_dict_chapters.items():
                if isinstance(v, str):
                    if v != "":
                        v = [int(x) for x in v.split("-")]
                    else:
                        v = []

                # PATH CHAPTERS OF COMIC ON DISC,
                # CAST DIRECTORIES NAMES TO FLOAT.
                if len(v) > 0:
                    for chapterObj in comicObj.chapters:

                        self.__chapter_to_volume(
                                    volume=k,
                                    chapter=chapterObj,
                                    start=float(v[0]),
                                    end=float(v[1])
                                )

                # IF volume is given but not chapters indicators is given.
                elif len(v) == 0:
                    if len(self.volumes) == 0:
                        volume_key = 1
                    else:
                        volume_key = list(self.volumes.keys())[-1] + 1

                    chapters_ = [
                                    i for i in comicObj.chapters
                                    if i.id not in self.chapters_in_volume
                                ]

                    self.volumes[volume_key] = Volume(
                                                    volume=volume_key,
                                                    list_chapters=chapters_
                                                )

                    self.chapters_in_volume += [
                                                i.id for i in comicObj.chapters
                                            ]
                    break

                else:
                    # ERROR:
                    #   if the volume is specified but only the chapter start
                    #   indicator is specified.
                    msg = 'Must deliver numeric *start* and *end* indicator,\
                     in a list or text string (e.g. "1-2", [1-2]) or leave \
                     blank with an empty string or list or not indicate a \
                     volume.'
                    raise ValueError(msg)

            self.__chapters_wo_volume_and_chapter_indicator(comic=comicObj)

            return self.volumes

        except ValueError as e:
            print(e)
            self.clear()
            return None

    def __chapter_to_volume(
        self,
        volume: int,
        chapter: Chapter,
        start: float = None,
        end: float = None
    ) -> None:
        """
        """
        # print(volume, chapter, start, end)
        number_chapter = chapter.id

        if number_chapter not in self.chapters_in_volume:

            if start <= number_chapter <= end:
                # print('> ', volume, start, end, number_chapter)
                if volume not in self.volumes:
                    self.volumes[volume] = Volume(
                                                volume=volume,
                                                list_chapters=[]
                                            )
                    self.volumes[volume].add(chapter)
                else:
                    self.volumes[volume].add(chapter)

                self.chapters_in_volume.append(number_chapter)


    def __chapters_wo_volume_and_chapter_indicator(
        self,
        comic: Comic = None,
        volume: int = None
    ) -> None:
        """
        If volume is given but not chapters indicators is given.
        If some chapters are not in volumes, they are grouped in a single
        volume.

        Args
            comic: `Comic` instance.
            volume: integer, number of volume.

        """
        if volume is not None:
            volume_key = volume
        else:
            if len(list(self.volumes.keys())) == 0:
                volume_key = 1
            else:
                volume_key = list(self.volumes.keys())[-1] + 1

        for id_, chapter in self.chapters_wo_volume.items():
            if id_ not in self.chapters_in_volume:
                # print(chapter)

                if volume not in self.volumes:
                    # self.volumes[volume] = [chapter]
                    self.volumes[volume_key] = Volume(
                                                    volume=volume_key,
                                                    list_chapters=[chapter]
                                                )

                else:
                    self.volumes[volume_key].list_chapters.append(chapter)

                # add to `chapters_in_volume` list
                self.chapters_in_volume.append(chapter.id)
                # remove of `chapters_wo_volume` dict
                self.chapters_wo_volume.pop(chapter.id)
