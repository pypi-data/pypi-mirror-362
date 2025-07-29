# -*- coding: utf-8 -*-
"""
"""

from getpycomic.pages.base import BaseMeta


class NovelCool(metaclass=BaseMeta):

    language = "es"

    page_language = {
        "en": "https://www.novelcool.com",
        "es": "https://es.novelcool.com",
        "br": "https://br.novelcool.com",
        "it": "https://it.novelcool.com",
        "ru": "https://ru.novelcool.com",
        "de": "https://de.novelcool.com",
        "fr": "https://fr.novelcool.com",
    }

    # if the web page has several languages leave it blank
    base = ""

    # search_url = base + "/search/?wd=NONE&page=1&category_id=%2C1413"
    search_url = base + "/search/?wd=NONE"

# search
    # search_button = ".open-search-main-menu"  # css selector
    # input_search = "#blog-post-search > input:nth-child(1)"  # css selector
#

# list of comic matches in search
    content_page_divs_css = ".category-book-list"  # css selector

    items_comic_css = ".book-item"  # css selector
    info_comic_css = "div"  # css selector

    # pagination = ".pagination"  # css selector
#


# comic and list of chapters
    # title_comic = ".post-title > h1:nth-child(2)"  # css selector
    chapters_content_ul_class = [
        ".chapter-item-list",  # class selector
    ]

    button_show_all_chapters = None

    chapter_css = [
        "div.chp-item:nth-child(n)",  # class selector
    ]

    chapter_name_class = "div > div > span:nth-child(1)"
    chapter_link_class = "a:nth-child(1)"
#

# into chapter page
    container_selector_lector = ".post-content-body"
    chapter_selector_lector_button = "a"  # css selector

    container_images_div_css = "#viewer"  # css selector

    # index pages
    index_pages = ".btn > span:nth-child(1) > em:nth-child(1) > a:nth-child(1)"
    # select
    selected_tag = ".change_pic_no"
    # option load 1 images
    options_select = "option:nth-child(n)"
    # # option load 10 images
    # "option:nth-child(4)"
