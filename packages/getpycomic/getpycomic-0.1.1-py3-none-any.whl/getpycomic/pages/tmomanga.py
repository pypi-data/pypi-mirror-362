# -*- coding: utf-8 -*-
"""
"""

from getpycomic.pages.base import BaseMeta


class TmoManga(metaclass=BaseMeta):

    base = "https://tmomanga.com"
    search_url = base + "/biblioteca?search=NONE"

# search
    # search_button = ".open-search-main-menu"  # css selector
    # input_search = "#blog-post-search > input:nth-child(1)"  # css selector
#

# list of comic matches in search
    content_page_divs_css = ".row-eq-height"  # css selector

    items_comic_css = "div.col-xl-3:nth-child(n)"  # css selector
    info_comic_css = ".h5 > a"  # css selector

    # pagination = ".pagination"  # css selector
#


# comic and list of chapters
    # title_comic = ".post-title > h1:nth-child(2)"  # css selector
    chapters_content_ul_class = [
        ".sub-chap",  # class selector

    ]

    button_show_all_chapters = None

    chapter_css = [
        "li.wp-manga-chapter:nth-child(n)",  # class selector

    ]

    chapter_name_class = "a:nth-child(1)"  # class selector
    chapter_link_class = None  # class selector
#

# into chapter page
    # content_images_comic_css = ".reading-content"  # css selector

    container_selector_lector = None
    chapter_selector_lector_button = None


    container_images_div_css = "#images_chapter"  # css selector


    # index pages
    index_pages = None
    # select
    selected_tag = None
    # option load 1 images
    option_selected = None
#
