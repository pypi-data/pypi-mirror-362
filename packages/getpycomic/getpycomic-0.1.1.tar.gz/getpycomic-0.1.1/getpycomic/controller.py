# -*- coding: utf-8 -*-
"""

"""

from getpycomic.models import (
        Comic,
        Chapter,
        ImageChapter
    )

# from getpycomic.imagehandler import ImagesHandler
from getpycomic.ziphandler import ZipHandler
from getpycomic.sorter_volume_chapter import VolumesSorter
from getpycomic.requests_data import RequestsData
from getpycomic.pathclass import PathClass
from getpycomic.status import Status

from getpycomic.utils import (
    get_user_agent,
    get_binary_firefox_and_geckodriver_path
)

from getpycomic.downloader import Downloader

from getpycomic.errorhandlerdecorator import register_error

# ENGINES
from getpycomic.engines import (
    Selenium,
)
#

from getpycomic.supported_webs import Supported_Webs

from time import sleep
from math import ceil
import re

from threading import Lock
import multiprocessing

import unicodedata

from typing import (
        List,
        Union,
        Literal,
    )

FilterTypes = Literal["id", "xpath", "tag_name", "css_selector"]




class GetPyComic:
    """
    """

    DIRECTORY = "GetPyComic"

    def __init__(
        self,
        web: Literal["tmomanga", "zonatmo", "novelcool"] = "tmomanga",
        engine: Literal["selenium", "playwright"] = "selenium",
        language: Literal["en", "es", "br", "it", "ru", "de", "fr"] = "es",
        binary_firefox_path: str = None,
        show: bool = True,
        setup: bool = True,
        verbose: bool = False,
        debug: bool = False,
    ) -> None:
        """
        """
        self.verbose = verbose
        self.debug = debug
        self.language = language
        self.binary_firefox = None

        self.DIRECTORY_GETPYCOMIC = ""

        self.web_site = None

        self.scraper = None

        self.current_comic = None  # `Comic` instance

        self.show = show  # show gui scraper
        self.setup = setup  # setup scraper

        self.parent_path = PathClass.dirname(path=__file__)
        # print('--> ', self.parent_path)

        # Selenium
        firefox_geckodriver_paths = get_binary_firefox_and_geckodriver_path(
                                                parent_path=self.parent_path
                                            )

        binary_location = firefox_geckodriver_paths["firefox_bin_path"]
        self.geckodriver_path = firefox_geckodriver_paths["geckodriver_path"]

        if binary_firefox_path is not None:
            self.binary_firefox = binary_firefox_path


        self.plugins_base = PathClass.join(
                                    self.parent_path,
                                    "drivers",
                                    "plugins"
                                )

        self.plugins_paths = [
                                PathClass.join(self.plugins_base, i)
                                for i in PathClass.listdir(self.plugins_base)
                            ]
        #

        self.status = Status(
                            controller=self,
                            base_path=self.parent_path,
                            language=self.language,
                        )

        self.set_base_dir()

        self.select_web(web)

        if setup:
            self.change_engine(engine)

    @staticmethod
    def get_default_chapter_by_volume() -> None:
        return VolumesSorter.CHAPTERS_BY_VOLUME

    def close_scraper(self) -> None:
        """
        """
        if self.scraper is not None:
            if self.verbose or self.debug:
                print(f"Scraper `{self.scraper}` is closed.")
            self.scraper.close()

    def check_driver(self) -> bool:
        """
        """
        if self.scraper is None:
            return False
        if self.scraper.driver is None:
            return False
        return True

    def select_web(
        self,
        web: str
    ) -> None:
        """
        """
        self.web_site = Supported_Webs.get_web(web)

        # website with language url
        if hasattr(self.web_site, "language"):
            self.web_site.language = self.language
            self.web_site.base = self.web_site.page_language[self.web_site.language]
            self.web_site.search_url = f"{self.web_site.base}{self.web_site.search_url}"


    def change_engine(
        self,
        engine: Literal["selenium", "playwright"]
    ) -> None:
        """
        """
        if self.scraper is not None:
            self.close_scraper()
            self.scraper = None

        if engine == "selenium":
            current_scraper = Selenium(
                                    geckodriver=self.geckodriver_path,
                                    binary=self.binary_firefox,
                                    plugins=self.plugins_paths,
                                    show=self.show,
                                    setup=self.setup,
                                    status=self.status,
                                    debug=self.debug,
                                )
        elif engine == "playwright":
            current_scraper = None

        self.scraper = current_scraper

        if self.debug or self.verbose:
            print("Scraper: ", self.scraper)

    def set_base_dir(
        self,
        path: str = None
    ) -> None:
        """
        """
        if path is None:
            new_base = PathClass.join(
                                    PathClass.get_home,
                                    GetPyComic.DIRECTORY
                                )
        else:
            new_base = PathClass.join(
                                    PathClass.get_home,
                                    path
                                )
        self.DIRECTORY_GETPYCOMIC = new_base
#
#  scraper
#
    # @register_error("search")
    def search(
        self,
        search: str,
        page: int = 1,
    ) -> list:
        """
        """
        if self.debug or self.verbose:
            print(f"Searching: `{search}` on `{self.web_site}`", )

        if self.check_driver():

            normalize = unicodedata.normalize("NFKD", search)
            search = ''.join(
                            [c for c in normalize
                                if not unicodedata.combining(c)
                            ]
                        )
            search = search.replace(" ", "+").replace(".", "")

            search = search + f"&page={page}"

            results = self.scraper.search(
                    string=search,
                    webclass=self.web_site,
                )

            return results

    # @register_error("get_chapters")
    def get_chapters(
        self,
        comic: Comic,
        n_chapters: int = None,
        range: List[int] = None,
        update: bool = False,
    ) -> Comic:
        """
        """
        if self.check_driver() and isinstance(comic, Comic):

            if self.debug or self.verbose:
                print("Getting chapters of ", self.current_comic)

            self.current_comic = comic

            self.scraper.get_chapters(
                                comic=comic,
                                webclass=self.web_site,
                                n_chapters=n_chapters,
                                range=range,
                                update=update,
                            )
            try:
                self.status.last_chapter = comic.chapters[-1].id
            except IndexError:
                self.status.last_chapter = None

            return comic

    # @register_error("get_images")
    def get_images(
        self,
        comic: Comic = None,
    ) -> Comic:
        """
        """
        if self.debug or self.verbose:
            print("get_images ", self.scraper)

        if self.check_driver():

            if comic is None:
                comic = self.current_comic

            for ch in comic.chapters:
                self.scraper.get_images(
                                    chapter=ch,
                                    webclass=self.web_site,
                                )
            return comic

    @property
    def get_current_comic(self) -> list:
        """
        """
        return self.current_comic
#
#
#
    def save_comic(
        self,
        comic: Comic = None,
        image_size: Literal["original", "small", "medium", "large"] = "original",
        n_threads: int = None,
    ) -> None:
        """
        """
        if n_threads is None:
            n_threads = max(1, multiprocessing.cpu_count() // 2)

        if self.debug:
            print(f"> save_comic: n_threads: {n_threads}")

        if comic is None:
            comic = self.current_comic

        if comic.chapters == []:
            return

        domain = re.findall(
                            r'([\w-]+)(?=\.\w{2,3}(?:\.\w{2})?$)',
                            self.web_site.base,
                            re.IGNORECASE
                        )

        if domain:
            web_name_ = domain[0]
        else:
            web_name_ = "-"

        comic_path = PathClass.join(
                                    PathClass.get_desktop(),
                                    GetPyComic.DIRECTORY,
                                    f"{comic.name}-{web_name_}"
                                )

        comic.path = comic_path

        PathClass.makedirs(path=comic_path)

        for chapter in comic.chapters:

            chapter_dir = PathClass.join(
                                        comic_path,
                                        chapter.name
                                        )

            PathClass.makedirs(path=chapter_dir)

            chapter.path = chapter_dir

        user_agent = get_user_agent()

        if self.web_site.base[-1] != "/":
            refer_site = self.web_site.base + "/"
        else:
            refer_site = self.web_site.base

        header_request = {
                            "Referer": refer_site,  # avoid hotlinking
                            'User-Agent': user_agent,
                        }

        n_chapters = len(comic.chapters)

        n_images = sum([i.amount_images() for i in comic.chapters])

        # print(n_chapters, n_images)
        # progress bar
        lock = Lock()
        index_progress = [0]

        threads_list = []
        if n_chapters < 20:
            downloader_thread = Downloader(
                                        chunk_chapters=comic.chapters,
                                        header=header_request,
                                        sizeImage=image_size,
                                        debug=self.debug,
                                        daemon=True,
                                        lock=lock,
                                        total_images=n_images,
                                        index_image=index_progress,
                                    )

            threads_list.append(downloader_thread)
            downloader_thread.start()

        else:
            chunk_chapters = ceil(n_chapters / n_threads)

            for i in range(0, n_chapters, chunk_chapters):
                chunk = comic.chapters[0 + i : i + chunk_chapters]

                downloader_thread = Downloader(
                                            chunk_chapters=chunk,
                                            header=header_request,
                                            sizeImage=image_size,
                                            debug=self.debug,
                                            daemon=True,
                                            lock=lock,
                                            total_images=n_images,
                                            index_image=index_progress,
                                        )

                threads_list.append(downloader_thread)
                downloader_thread.start()


        # show progress bar in CLI
        while True:
            with lock:
                percent = (index_progress[0] / n_images) * 100

                msg = "\r\tImages: "
                msg += f"{index_progress[0]}-{n_images}"
                msg += f"   ({percent:.2f}%)"
                print(msg, end="", flush=True)
                if index_progress[0] >= n_images:
                    print("\n\n")
                    break
            sleep(0.2)


        # initialize work on threads
        for th in threads_list:
            th.join()


    def sorter_by_volumes(
        self,
        comic: Comic = None,
        chapters_by_volume: int = None,
        volumes_dict_chapters: dict = None,
    ) -> Comic:
        """
        Sorter chapters downloaded into volumes using a diccionaries of digits,
        these values indicate the chapters to be stored in volumes.

        To determine the volume is a single digit (`int`), to determine the
        chapters a string of digits separated by a hyphen or a list of digits
        (`int`) can be used.

        If you do not give one, by default all chapters are merged into one
        volume.

        Chapter information by volume can be obtained at `https://comick.io/`.

        Examples:

            # Single Comic
            sorter_by_volumes(
                volumes_dict_chapters={1: [1, 2], 2: [3, 5]}
            )

            sorter_by_volumes(
                volumes_dict_chapters={1: "1-2", 2: "3-5"}
            )

        Args
            comic: directory path (str) or instance of `Comic`, if not given,
                   the current instance of `Comic` will be used.
            chapters_by_volume: int, number of chapter by volume. Has priority
                                over `volumes_dict_chapters`.
            volumes_dict_chapters: dictionary for one comic book. The number of
                                elements must be exactly the same.

        Returns
            dict: returns a dicctionary with volume number as key and `Volume`
                  instance as value.
        """
        # print(volumes_dict_chapters, chapters_by_volume, comic)
        if isinstance(comic, str):
            comic_ = GetPyComic.build_Comic_from_path(path=comic)
            if comic_ is None:
                return
            comic = comic_

        if comic is None:
            comic = self.current_comic


        ch_vl = VolumesSorter()

        if chapters_by_volume is not None and isinstance(chapters_by_volume, int):
            chapters_by_volume = chapters_by_volume
        elif volumes_dict_chapters is not None and isinstance(volumes_dict_chapters, dict):
            volumes_dict_chapters = volumes_dict_chapters
        else:
            chapters_by_volume = None
            volumes_dict_chapters = None

        # print('#### > ', chapters_sorter)

        volumes_chapters = ch_vl.sorter(
                                comicObj=comic,
                                volumes_dict_chapters=volumes_dict_chapters,
                                chapters_by_volume=chapters_by_volume
                            )

        comic.volumes = volumes_chapters
        self.current_comic = comic

        return comic


    def to_cbz(
        self,
        comic: Comic = None,
        preserve_images: bool = True
    ) -> None:
        """
        Convert to CBZ file.

        If CBZ files exist in the directory, get the last index of the filename
        and rebuild the volume dictionary of the `Comic` instance.

        """

        if comic is None:
            comic = self.current_comic
        # print(comic.name)
        # print(comic.link)
        # print(comic.chapters)
        # print(comic.path)
        # print(comic.volumes)

        if comic.volumes is None or comic.volumes == {}:
            return


        # print("> ", comic.volumes)

        if PathClass.exists(comic.path):
            files_ = PathClass.get_files_recursive(
                                        extensions=".cbz",
                                        directory=comic.path
                                    )

            if files_:
                nums = [
                            int(re.findall(r'-(\d+)\(', i)[0])
                            for i in files_
                            if re.findall(r'-(\d+)\(', i)
                        ]
                if nums:
                    start = max(nums) + 1
                    size = len(comic.volumes) + start
                    if start > max(comic.volumes.keys()):
                        new_volumes = dict(
                                        zip(
                                            [i for i in range(start, size)],
                                            comic.volumes.values()
                                        )
                                    )
                        comic.volumes = new_volumes

        if self.debug:
            print("> ", comic.name, comic.volumes)

        for id_volume, volumechapterObj in comic.volumes.items():

            # print(f"{volume}".zfill(3), [i.path for i in chapters])

            if volumechapterObj.n_chapters > 0:

                cbz_name = "%s-%s(%s).cbz" % (
                    comic.name,
                    f"{id_volume}".zfill(3),
                    volumechapterObj.get_range_chapters()
                )

                path_cbz = PathClass.join(
                                        comic.path,
                                        cbz_name
                                    )

                if self.verbose:
                    print(">> ", path_cbz)

                ZipHandler.to_zip(
                        cbz_path=path_cbz,
                        list_chapters=volumechapterObj.list_chapters
                    )

                if preserve_images is False:
                    self.delete_images(
                                list_chapters=volumechapterObj.list_chapters
                            )

    def delete_images(
        self,
        list_chapters: List[Chapter]
    ) -> None:
        """
        """
        for chapter in list_chapters:
            # print('--> ', PathClass.absolute_path(path=chapter.path))
            PathClass.delete_directory(
                    path=PathClass.absolute_path(path=chapter.path)
                )


    @staticmethod
    def build_Comic_from_path(
        path: str
    ) -> Union[Comic, None]:
        """
        Builds the `Comic` instance from a valid directory path (str). If `path`
        is not a directory returns `None`.

        Args
            path: str, directory path.

        Returns
            Comic: `Comic` instance.
            None: if the `path` argument is not a directory path.
        """
        if not PathClass.is_dir(path):
            return None

        patron = re.compile(r'(-\w+|-)$', re.IGNORECASE)

        comic = Comic()
        comic.name = patron.split(PathClass.basename(path))[0]
        comic.path = PathClass.absolute_path(path)


        try:
            list_of_dirs = sorted(
                                [
                                    i for i in PathClass.listdir(path)
                                    if PathClass.is_dir(PathClass.join(path, i))
                                ],
                                key=lambda x: float(x)
                            )
        except Exception as e:
            return None

        for dir in list_of_dirs:
            chapter_path = PathClass.join(comic.path, dir)
            if not PathClass.is_dir(chapter_path):
                continue

            images = PathClass.listdir(chapter_path)
            images.sort(key=lambda x: int(PathClass.splitext(x)[0]))

            images_instances = [
                                ImageChapter(
                                        id=int(PathClass.splitext(img)[0]),
                                        name=PathClass.splitext(img)[0],
                                        extension=PathClass.splitext(img)[1],
                                        link=None,
                                        path=PathClass.join(chapter_path, img),
                                    )
                                    for img in images
                                ]

            ch = Chapter(
                    id=float(dir),
                    name=str(dir),
                    link=None,
                    images=images_instances,
                    path=chapter_path,
                )
            comic.chapters.append(ch)

        return comic

    def to_json(self) -> None:
        """
        """
        if self.debug or self.verbose:
            print("Save status on json.")
        self.status.to_json()

    def to_load(self) -> None:
        """
        """
        self.status.to_load()

    def __str__(self) -> str:
        """
        """
        return "GetPyComic: ID: %s, Site: %s, Scraper: %s, Lang: %s, Show: %s, Setup: %s, Verbose: %s" % (
                                    str(id(self)),
                                    self.web_site.base,
                                    self.scraper,
                                    self.language,
                                    self.show,
                                    self.setup,
                                    self.verbose,
                                )

    def __repr__(self) -> str:
        """
        """
        return "<[ %s ]>" % self.__str__()
