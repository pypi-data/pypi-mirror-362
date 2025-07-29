# -*- coding: utf-8 -*-
"""
"""

from getpycomic.imagehandler import ImagesHandler
from getpycomic.requests_data import RequestsData
from getpycomic.pathclass import PathClass

from threading import Thread, Lock

from typing import Literal


class Downloader(Thread):

    def __init__(
        self,
        chunk_chapters: list,
        header: dict,
        sizeImage: Literal["original", "small", "medium", "large"] = "original",
        debug: bool = False,
        daemon: bool = True,
        lock: Lock = None,
        index_image: list = None,
        total_images: int = 1,
    ) -> None:
        """
        """
        Thread.__init__(self, daemon=daemon)
        self.imagehandler = ImagesHandler()
        self.chunk_chapters = chunk_chapters
        self.sizeImage = sizeImage
        self.header = header
        self.debug = debug

        self.lock = lock
        self.index_image = index_image
        self.total_images = total_images

    def run(self) -> None:
        """
        Gets the images from the URL and saves them.
        """
        if self.debug:
            print(self)

        for chapter in self.chunk_chapters:

            for image in chapter.images:
                # image.id
                # image.name
                # image.extension
                # image.link
                # print(image.name, image.extension)

                image.extension = '.jpg'

                image_path_ = PathClass.join(
                                            chapter.path,
                                            image.get_name()
                                        )
                image.path = image_path_

                if PathClass.exists(image_path_) is False:

                    # get image data from url
                    data = RequestsData.request_data(
                            header=self.header,
                            link=image.link
                        )

                    if data is not None:
                        new_image_data_ = self.imagehandler.new_image(
                                                    currentImage=data,
                                                    extension="jpeg",
                                                    # sizeImage='small'
                                                    sizeImage=self.sizeImage
                                                )

                        self.imagehandler.save_image(
                                                path_image=image.path,
                                                image=new_image_data_
                                            )

                if self.lock:
                    with self.lock:
                        self.index_image[0] = self.index_image[0] + 1
