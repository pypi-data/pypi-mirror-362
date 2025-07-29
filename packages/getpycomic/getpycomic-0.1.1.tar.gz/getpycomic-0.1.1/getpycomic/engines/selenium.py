# -*- coding: utf-8 -*-
"""

Chrome  : chromedriver  - chromedriver.chromium.org
Firefox : geckodriver   - github.com/mozilla/geckodriver
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys


from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)

from selenium.webdriver.remote.webelement import WebElement


from time import sleep
import re
from uuid import uuid4
import random
from math import ceil
from queue import Queue
import multiprocessing

from getpycomic.engines.base import Base

from getpycomic.models import (
        Comic,
        Chapter,
        ImageChapter
    )

from getpycomic.pathclass import PathClass
from getpycomic.errorhandlerdecorator import register_error
from getpycomic.status import Status


from getpycomic.utils import (
    normalize_number,
    get_user_agent
)

from getpycomic.engines.thread_selenium import ThreadSelenium


from typing import (
        List,
        Union,
        Literal,
    )


FilterTypes = Literal["id", "xpath", "tag_name", "css_selector"]


class Selenium(Base):
    """
    """

    def __init__(
        self,
        geckodriver: str,
        binary: str = None,
        plugins: list = [],
        show: bool = True,
        setup: bool = True,
        status: Status = None,
        debug: bool = False,
    ) -> None:
        """
        """
        self.driver = None
        self.show = show
        self.status = status
        self.debug = debug

        self.binary = binary
        self.geckodriver = geckodriver
        self.plugins = plugins

        if setup:
            try:
                self.setup()
            except Exception as e:
                print("Error during setup ", e)

        sleep(1)

    def close(self) -> None:
        """
        """
        if self.driver is not None:
            # self.driver.close()
            self.driver.quit()
            self.driver = None

    @register_error("setup")
    def setup(self) -> None:
        """
        """
        servicio = Service(executable_path=self.geckodriver)

        user_agent = get_user_agent()

        op = Options()

        # sets binary of navegator
        if self.binary is not None:
            op.binary_location = self.binary

        profile = FirefoxProfile()

        ######### Chrome
        # if self.show is False:
        #     op.add_argument('--headless')
        # op.add_argument('--disable-gpu')
        # op.add_argument('--blink-settings=imagesEnabled=false')
        # user-agent
        # op.add_argument(f'user-agent={user_agent}')
        # avoid cloudflare
        # op.add_argument('--disable-blink-features=AutomationControlled')
        # op.set_preference('useAutomationExtension', False)
        ######### Chrome

        # Firefox
        # change user-agent
        profile.set_preference('general.useragent.override', user_agent)
        # disable pop-ups
        profile.set_preference("dom.webnotifications.enabled", False)
        # don't load images
        profile.set_preference("permissions.default.image", 2)
        # disable audio
        profile.set_preference("media.volume_scale", "0.0")
        # avoid webdriver detection
        profile.set_preference("dom.webdriver.enabled", False)
        # prevents device information from being sent
        profile.set_preference("media.navigator.enabled", False)
        # nothing
        profile.set_preference("useAutomationExtension", False)
        # disables automation advises
        profile.set_preference("media.navigator.permission.disabled", True)

        # forces use Tabs.
        profile.set_preference("browser.link.open_newwindow", 3)  # 3 = nueva pestaña
        profile.set_preference("browser.link.open_newwindow.restriction", 0)
        profile.set_preference("browser.tabs.loadInBackground", False)

        # Helps prevent real IP leaks and reduces fingerprinting vectors.
        profile.set_preference("media.peerconnection.enabled", False)
        # protection against tracking
        profile.set_preference("privacy.trackingprotection.enabled", True)
        # webpage loading strategy
        profile.set_preference("webdriver.load.strategy", "normal")

        # disable console logs
        profile.set_preference("devtools.console.stdout.content", False)

        # sets profice to Options
        op.profile = profile

        # page load strategy
        op.page_load_strategy = 'eager'

        # enable GUI
        if self.show is False:
            op.add_argument("--headless")

        # create the driver
        self.driver = webdriver.Firefox(options=op, service=servicio)
        self.driver.set_window_size(1280, 720)

        # install plugins - firefox
        for path in self.plugins:
            self.driver.install_addon(path)

        # deletes `navigator.webdriver` attribute
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        self.driver.execute_script("""
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
        """)

        # hardwareConcurrency, maxTouchPoints
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'hardwareConcurrency', {
              get: () => 8,
            });
            Object.defineProperty(navigator, 'maxTouchPoints', {
              get: () => 1,
            });
        """)

        # spoof WebGL vendor/renderer
        self.driver.execute_script("""
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter){
              if(parameter === 37445) return "Intel Inc.";
              if(parameter === 37446) return "Intel Iris OpenGL Engine";
              return getParameter(parameter);
            };
        """)

        # Canvas fingerprint spoof
        self.driver.execute_script("""
            const getImageData = CanvasRenderingContext2D.prototype.getImageData;
            CanvasRenderingContext2D.prototype.getImageData = function() {
              const data = getImageData.apply(this, arguments);
              data.data[0] += 1; // tiny change
              return data;
            };
        """)

        ###### test scraper
        # self.driver.get("https://bot.sannysoft.com/")
        # print("Headless:", self.driver.capabilities.get("moz:headless"))
        # self.driver.save_screenshot(f"{uuid4()}.png")
        ######

    def wait_for_element(
        self,
        type: List[FilterTypes],
        html_element: str,
        time: int = 10
    ) -> Union[WebElement, None]:
        """
        """
        filter = {
            "id": By.ID,
            "xpath": By.XPATH,
            "tag_name": By.TAG_NAME,
            "css_selector": By.CSS_SELECTOR
        }

        try:
            filter_type = filter[type]
            element = WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located(
                    (filter_type, html_element)
                )
            )
            return element
        except (KeyError, TimeoutException):
            return None


    def wait_to_load_content_change_tab(
        self,
        element: str,
        time: int = 10
    ) -> None:
        """
        """
        WebDriverWait(self.driver, time).until(
                            lambda driver: len(driver.window_handles) > 1
                        )

        # print("> wait_to_load_content_change_tab", self.driver.window_handles)

        last_tab = self.driver.window_handles[-1]

        self.driver.switch_to.window(last_tab)

        # headless check change to new tab
        # self.driver.save_screenshot(f"{uuid4()}.png")

        for i in range(0, 3):

            if self.driver.current_url.endswith("/paginated"):
                self.driver.get(
                        self.driver.current_url.replace("/paginated", "/cascade")
                    )

            item = self.wait_for_element(
                        type="css_selector",
                        html_element=element
                    )

            # print("> ", item, self.driver.current_url)

            if item is not None:
                return

            sleep(0.3)

    def element_find_elements(
        self,
        element: WebElement,
        selectors: list
    ) -> list:
        """
        Searches for elements using a `WebElement` parent element and CSS
        selector, returns a list with elements inside the parent element.
        """
        for i in range(0, 3):
            for selector in selectors:
                results = element.find_elements(
                                        By.CSS_SELECTOR,
                                        selector
                                    )
                # print(selector, len(results))
                if results != []:
                    return results
                sleep(0.5)
        return []

    def iterator_find_elements(
        self,
        type: List[FilterTypes],
        selectors: list
    ) -> Union[WebElement, None]:
        """
        Searches for a `WebElement` parent element using a list of CSS
        selectors.
        """
        for selector in selectors:
            element = self.wait_for_element(
                        type="css_selector",
                        html_element=selector
                    )
            if element is not None:
                return element
        return None

    @register_error("search")
    def search(
        self,
        string: str,
        webclass: object
    ) -> list:
        """
        """
        results = []

        url = webclass.search_url.replace("NONE", string)

        # print(">> search", url)

        self.driver.get(url)

        sleep(1)

        if self.debug:
            print("> search ", webclass)

        if "novelcool" in url:
            self.driver.execute_script("window.stop();")


        div_content_comics = self.wait_for_element(
                                type="css_selector",
                                html_element=webclass.content_page_divs_css
                            )

        if div_content_comics is not None:
            items_list = div_content_comics.find_elements(
                                                By.CSS_SELECTOR,
                                                webclass.items_comic_css
                                            )

            for item in items_list:
                info_item = item.find_element(
                        By.CSS_SELECTOR,
                        webclass.info_comic_css
                    )

                try:
                    # novelcool
                    name = info_item.get_attribute("title")
                    link = info_item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                except Exception as e:
                    # zonatmo, tmomanga
                    name = info_item.get_attribute("innerText")
                    link = info_item.get_attribute("href")


                if "novelcool" in url and "novel" in name.lower():
                    continue

                name = name.split("\n")[0].title().replace(" ", "_")
                name = name.replace(":", "-")
                comic = Comic(
                        name=name,
                        original_name=name.split("\n")[0],
                        link=link
                    )
                results.append(comic)

        return results

    @register_error("get_chapters")
    def get_chapters(
        self,
        comic: Comic,
        webclass: object,
        n_chapters: List[int] = None,
        range: List[int] = None,
        update: bool = False
    ) -> Comic:
        """
        Gets chapters of `Comic` instance.
        Important: `n_chapters` has precedence over `range` parameter.

        Args:
            comic: `Comic` instance.
            webclass: engine to get data.
            n_chapters: positive integer or list of integers specifying the
                        chapters.
            range: list of two positives integers, sets range of chapters to
                   get, for example [1, 10].
            update: bool, gets only new chapters from the `Comic` chapter list.
                    It takes precedence over `n_chapters` and `range`.
                    Default is `False`.

        Returns:
            comic: `Comic` instance with updated chapters.
        """
        if self.debug:
            print("> get_chapters",
                        webclass,
                        n_chapters,
                        range,
                        update,
                    )

        if comic.link:
            self.driver.get(comic.link)

            self.status.comic_name = comic.name

            chapters_ul_list = self.iterator_find_elements(
                                type="css_selector",
                                selectors=webclass.chapters_content_ul_class
                            )


            try:
                button_show_ = chapters_ul_list.find_elements(
                                            By.CSS_SELECTOR,
                                            webclass.button_show_all_chapters
                                        )
                button_show_.click()

                sleep(0.5)
            except Exception as e:
                pass

            list_chapters = self.element_find_elements(
                                                element=chapters_ul_list,
                                                selectors=webclass.chapter_css
                                            )

            list_chapters = list_chapters[::-1]


            chapters_comic_list = []
            chapter_id = 1.0

            for li_item_ in list_chapters:

                try:
                    a_item_ = li_item_.find_element(
                                                By.CSS_SELECTOR,
                                                webclass.chapter_name_class
                                            )

                except NoSuchElementException as e:
                    a_item_ = li_item_.find_element(
                                                By.TAG_NAME,
                                                "div"
                                            )

                name_chapter = a_item_.get_attribute("innerText").strip()

                try:
                    link_item_ = li_item_.find_element(
                                                    By.CSS_SELECTOR,
                                                    webclass.chapter_link_class
                                                )
                    link_chapter = link_item_.get_attribute("href").strip()

                except Exception as e:
                    link_chapter = a_item_.get_attribute("href").strip()

                # gets the chapter number of the html element
                regex_number_ = re.findall(
                                    r'(?:ch(?:\.|ap|apter)?|cap(?:[íi]tulo)?|ep(?:\.|isode)?)\s*[:\-]?\s*(\d+(?:[.,]\d+)?)',
                                    name_chapter,
                                    re.IGNORECASE
                                )

                if regex_number_ != []:
                    chapter_number = float(normalize_number(regex_number_[0]))
                else:
                    chapter_number = chapter_id
                    chapter_id += 1


                self.status.chapter_id = link_chapter

                chapterObj = Chapter(
                                id=chapter_number,
                                name=f"{chapter_number}",
                                link=link_chapter
                            )

                if self.debug:
                    print("> ", name_chapter, chapter_number, link_chapter, chapterObj)

                chapters_comic_list.append(chapterObj)

            # natural sort
            chapters_comic_list.sort()
            chapters_comic = []

            if self.debug:
                print("Number of chapters ", len(chapters_comic_list))

            if update:
                chapters_comic = [
                                    item
                                    for item in chapters_comic_list
                                    if item.id > n_chapters[0]
                                ]

            else:
                if n_chapters is not None:
                    chapters_comic = [
                                        item
                                        for item in chapters_comic_list
                                        if item.id in n_chapters
                                    ]

                elif range is not None:
                    chapters_comic = [
                                item
                                for item in chapters_comic_list
                                if item.id > range[0] and item.id <= range[1]
                            ]
                else:
                    chapters_comic = chapters_comic_list

            # print(len(chapters_comic_list), len(chapters_comic))

            comic.chapters = chapters_comic

            # if more 50 chapters go to threading
            if len(comic.chapters) > 20:
                self.to_thread_scraping(
                                    comicObj=comic,
                                    webclass=webclass,
                                )
            else:
                self.iterate_get_chapter_images(
                                comicObj=comic,
                                webclass=webclass,
                            )

            return comic

    def iterate_get_chapter_images(
        self,
        comicObj: Comic,
        webclass: object,
        list_chapters: list = None,  # used by thread
        is_thread: bool = False,  # used by thread
    ) -> None:
        """
        """
        if self.debug:
            print("> iterate_get_chapter_images")

        chapters_comic_list = []

        # main tab of driver
        main_tab_ = self.driver.current_window_handle

        if list_chapters is None:
            list_chapters = comicObj.chapters

        for chapter in list_chapters:

            self.status.chapter_id = chapter.id

            # open chapter link to new tab for images
            self.driver.execute_script(
                                    f"window.open('{chapter.link}', '_blank');"
                                )
            # print("> ", self.driver.current_url, self.driver.window_handles)

            if webclass.container_selector_lector is not None:
                self.wait_to_load_content_change_tab(
                                    element=webclass.container_selector_lector,
                                    time=10
                                )

                container_selector_lector = self.wait_for_element(
                                type="css_selector",
                                html_element=webclass.container_selector_lector
                            )

                lectors_buttons = self.element_find_elements(
                                element=container_selector_lector,
                                selectors=[webclass.chapter_selector_lector_button]
                            )

                # randomize button list
                selected_id = random.randint(0, len(lectors_buttons)) - 1
                for i in range(0, random.randint(0, 10)):
                    random.shuffle(lectors_buttons)

                # move to button selected
                actions = ActionChains(self.driver)
                actions.move_to_element(lectors_buttons[selected_id]).perform()

                lectors_buttons[selected_id].click()

                sleep(1)

                # change to all images of page
                index_pages_label = self.wait_for_element(
                                            type="css_selector",
                                            html_element=webclass.index_pages
                                        )
                # print(index_pages_label)
                n_ = index_pages_label.get_attribute("innerText").split(" ")[-1]

                select_element = self.wait_for_element(
                                            type="css_selector",
                                            html_element=webclass.selected_tag
                                        )
                # print(select_element)

                options_select_ = self.element_find_elements(
                                        element=select_element,
                                        selectors=[webclass.options_select],
                                    )
                # print(options_select_)

                options_select_[0].click()

                if int(n_) > 10:
                    self.driver.execute_script(
                                "arguments[0].setAttribute('value', arguments[1])",
                                options_select_[-1],
                                n_
                            )
                    options_select_[-1].click()
                    sleep(1)

                # input(">>>>>>>>>>>>>>> ")
            else:
                # pages without lector selector
                self.wait_to_load_content_change_tab(
                                    element=webclass.container_images_div_css,
                                    time=10
                                )


            # real url of chapter
            url_chapter = self.driver.current_url

            chapter.link = url_chapter

            self.get_images(
                            chapter=chapter,
                            webclass=webclass,
                        )

            chapters_comic_list.append(chapter)

            if self.debug:
                print("> ", chapter, len(chapter.images))

            # close current tab
            self.driver.close()
            # return to main tab
            self.driver.switch_to.window(main_tab_)


        if is_thread is False:
            # natural sort
            chapters_comic_list.sort()
            comicObj.chapters = chapters_comic_list
        else:
            return chapters_comic_list

    @register_error("get_images")
    def get_images(
        self,
        chapter: Chapter,
        webclass: object,
    ) -> None:
        """
        """
        if self.debug:
            print("> get_images ", chapter)

        images_div_ = self.wait_for_element(
                                type="css_selector",
                                html_element=webclass.container_images_div_css
                            )

        if self.debug:
            print("> container is_displayed()", images_div_.is_displayed())

        chapter_images = []
        id_ = 1

        sleep(1)

        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        self.driver.execute_script(
            "window.lazySizes && lazySizes.loader.checkElems();"
        )


        list_images_ = self.element_find_elements(
                        element=images_div_,
                        selectors=["img"]
                    )

        # print("> images", len(list_images_))

        for img in list_images_:

            url_image = img.get_attribute('data-src')

            if url_image is None:
                url_image = img.get_attribute('src')

            # print("> ", url_image)
            name_, ext_ = PathClass.splitext(url_image)

            self.status.imagechapter_id = id_

            image = ImageChapter(
                                id=id_,
                                name=name_,
                                extension=ext_,
                                link=url_image
                            )
            # print(image)
            chapter_images.append(image)

            id_ += 1

        chapter.images = chapter_images


    def to_thread_scraping(
        self,
        comicObj: Comic,
        webclass: object,
        n_threads: int = None
    ) -> None:
        """
        """
        if n_threads is None:
            n_threads = max(1, multiprocessing.cpu_count() // 2)

        if self.debug:
            print(f"> to_thread_scraping: n_threads: {n_threads}")

        cookies = self.driver.get_cookies()

        n_chapters = len(comicObj.chapters)
        range_chapters = ceil(n_chapters / n_threads)


        threads_list = []
        queue = Queue()

        # print("> n_chapters", n_chapters)
        for i in range(0, n_chapters, range_chapters):
            if self.debug:
                print("> chapters range", 0 + i, i + range_chapters)

            chunk = comicObj.chapters[0 + i : i + range_chapters]

            # new instance Selenium class
            scraperInstance = Selenium(
                                    geckodriver=self.geckodriver,
                                    binary=self.binary,
                                    plugins=self.plugins,
                                    show=self.show,
                                    setup=False,
                                    status=self.status,
                                    debug=self.debug,
                                )

            # pass to thread:
            #       Selenium instance without setup
            #       queue to store Chapters instances with new data
            #       chunk_chapters chunk of chapters for this thread
            #       webclass template
            th = ThreadSelenium(
                            scraper=scraperInstance,
                            comicObj=comicObj,
                            cookies=cookies,
                            webclass=webclass,
                            container_queue=queue,
                            chunk_chapters=chunk,
                            debug=self.debug
                        )
            threads_list.append(th)
            th.start()

            sleep(0.5)

            #############  test
            # th.join()  # test
            # break      # test

        for th in threads_list:
            th.join()
            sleep(0.5)

        # copy `Chapter` instances on list
        items = []
        while not queue.empty():
            items.append(queue.get())

        # natural sort
        items.sort()
        comicObj.chapters = items
