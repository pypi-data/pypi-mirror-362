# -*- coding: utf-8 -*-
"""
"""

from getpycomic.pages.base import BaseMeta


class ZonaTmo(metaclass=BaseMeta):

    base = "https://zonatmo.com"
    search_url = base + "/library?title=NONE&_pg=1"

# search
    # search_button = ".open-search-main-menu"  # css selector
    # input_search = "#blog-post-search > input:nth-child(1)"  # css selector
#

# list of comic matches in search
    content_page_divs_css = "div.row:nth-child(3)"  # css selector

    items_comic_css = "div.element:nth-child(n)"  # css selector
    info_comic_css = "a:nth-child(1)"  # css selector

    # pagination = ".pagination"  # css selector
#


# comic and list of chapters
    # title_comic = ".post-title > h1:nth-child(2)"  # css selector
    chapters_content_ul_class = [
        "#chapters",  # class selector
        ".list-group",  # class selector

    ]

    button_show_all_chapters = "#show-chapters"  # button show chapters

    chapter_css = [
        ".list-group-item.p-0.bg-light.upload-link",  # class selector
        ".list-group-item.upload-link"
    ]

    chapter_name_class = ".px-2.py-3.m-0"  # class selector
    chapter_link_class = ".btn.btn-default.btn-sm"  # class selector
#

# into chapter page
    # content_images_comic_css = ".reading-content"  # css selector

    container_selector_lector = None
    chapter_selector_lector_button = None

    container_images_div_css = "#main-container"  # css selector

    # index pages
    index_pages = None
    # select
    selected_tag = None
    # option load 1 images
    option_selected = None
#
