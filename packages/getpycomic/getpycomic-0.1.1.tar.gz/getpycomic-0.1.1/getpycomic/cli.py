# -*- coding: utf-8 -*-
"""
"""

from getpycomic.controller import GetPyComic
from getpycomic.utils import (
    parser_volumes,
    parser_chapter
)
from getpycomic.supported_webs import Supported_Webs

import argparse
import sys
import os


def clear_console():
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")



def selector_interactive(
    controller: GetPyComic,
    search: str,
    page: int = 1,
) -> None:
    """
    """
    items = controller.search(search=search, page=page)
    if items is None:
        items = []

    clear_console()

    msg = "-" * 40 + "\n"
    msg += " " * 10 + f"Elements found: {search}\n"

    for i, item in enumerate(items, start=1):
        msg += f" {str(i).rjust(3)})  {item.original_name}\n"

    msg += f"Page: {page}\n".center(40)

    msg += "\n[p] Prev | [n, Enter] Next | [q, quit, x] Quit"

    print(f"\r{msg}\n", end="", flush=True)

    sel = input(">>> ", ).strip().lower()

    if sel.isdigit():
        idx = int(sel)
        if 1 <= idx <= len(items):
            return items[idx - 1]

    elif sel in ["q", "quit", "x"]:
        return None

    elif sel in ["n", ""]:
        page = page + 1
    elif sel == "p" and page > 0:
        page = page - 1

    return selector_interactive(
                        controller=controller,
                        search=search,
                        page=page
                    )

def main() -> None:
    """
    """
    main_parser = argparse.ArgumentParser(
        prog="getpycomic",
        description="Gets manga/comic from web to CBZ files.",
        epilog="You can read your manga/comics wherever you want."
    )


    main_parser.add_argument(
        "-n",
        "--name_or_path",
        required=True,
        nargs="+",
        help="Name of the manga/comic or path of the manga/comic downloaded",
    )

    main_parser.add_argument(
        "-w",
        "--web",
        choices=Supported_Webs.get_keys(),
        default=Supported_Webs.get_keys()[0],
        help=f"Select website. Default `{Supported_Webs.get_keys()[0]}`"
    )

    main_parser.add_argument(
        "-c",
        "--chapter",
        default="all",
        help="Chapters: `all`, `1,5`, `5+` `1-5`. Default `all`.",
        type=str,
    )

    msg = "Indicate how the chapters will be put together by volume in the "
    msg += "CBZ file. By default, each volume has "
    msg += f"`{GetPyComic.get_default_chapter_by_volume()}` chapters."
    msg += "\nFor example: 1:[1,4],2:[5,9]"

    main_parser.add_argument(
        "-v",
        "--volumes",
        default=None,
        nargs="+",
        help=msg
    )

    main_parser.add_argument(
        "--no-cbz",
        default=False,
        action="store_true",
        help="It only downloads chapters and does not create CBZ files."
    )

    main_parser.add_argument(
        "-e",
        "--engine",
        choices=["selenium"],
        default="selenium",
        help="Select engine to get data. Default `selenium`."
    )

    main_parser.add_argument(
        "-l",
        "--language",
        choices=["en", "es", "br", "it", "ru", "de", "fr"],
        default="es",
        help="Select language. Default `es`."
    )

    main_parser.add_argument(
        "--no-download",
        default=False,
        action="store_true",
        help="It does not configure the motor and does not prepare it."
    )

    main_parser.add_argument(
        "-s",
        "--show",
        default=False,
        action="store_true",
        help="Show engine or not. Default is no."
    )

    main_parser.add_argument(
        "--verbose",
        default=False,
        action="store_true",
        help="Displays messages of all operations."
    )

    main_parser.add_argument(
        "-i",
        "--interactive",
        default=False,
        action="store_true",
        help="Interactive Prompt for manga/comics search. By default the first item found is used."
    )

    main_parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="Show more messages for debug."
    )

    main_parser.add_argument(
        "--no-preserve",
        default=True,
        action="store_false",
        help="Preserve or not the manga/comic images. By default the images are preserved."
    )

    main_parser.add_argument(
        "--size",
        default="original",
        choices=["original", "small", "medium", "large"],
        help="Select the size of the image. Default is `original`."
    )

    main_parser.add_argument(
        "--firefox-bin",
        default=None,
        help="Binary path of Firefox."
    )


    args = main_parser.parse_args()

    # print(args)

    web = args.web # ='tmomanga'
    engine = args.engine # ='selenium'
    language = args.language # ='es'
    show = args.show # =False
    no_download = args.no_download # =False
    verbose = args.verbose # =False

    no_preserve = args.no_preserve
    size_image = args.size

    name = ' '.join(args.name_or_path) # ='a'

    chapter = args.chapter # = "all", "1", "5+" "1-5", "1,5"

    volumes = args.volumes
    no_cbz = args.no_cbz

    interactive = args.interactive # False

    debug = args.debug

    firefox_bin = args.firefox_bin


####
    chapters_dict = parser_chapter(string=chapter)
    matrix_dict = parser_volumes(string=volumes)

    if debug:
        print("> ", args, chapters_dict, matrix_dict)
    if verbose:
        print("> ", chapters_dict, matrix_dict)

    getpycomic = None
    try:
        getpycomic = GetPyComic(
                                web=web,
                                engine=engine,
                                language=language,
                                show=show,
                                setup=True if no_download is False else False,
                                verbose=verbose,
                                binary_firefox_path=firefox_bin,
                            )
        if no_download is False:
            print(f"> Searching in `{web}`...")
            if interactive:
                selected = selector_interactive(
                                            controller=getpycomic,
                                            search=name,
                                            page=1
                                        )

            else:
                items = getpycomic.search(search=name, page=1)
                if items is None:
                    print(">> An error has occurred in the search engine.")
                    return
                if items == []:
                    print(f">> No element found using: `{name}`.\n\n")
                    getpycomic.close_scraper()
                    return

                # selected first item
                selected = items[0]

            if debug:
                print(">> Selected element: ", selected)

            print("> Getting chapters...")
            getpycomic.get_chapters(
                                comic=selected,
                                n_chapters=chapters_dict["n_chapters"],
                                range=chapters_dict["range"],
                                update=chapters_dict["update"]
                            )

            if debug:
                print(">> ", selected)

            getpycomic.close_scraper()

            print("> Downloading...")
            getpycomic.save_comic(
                                comic=selected,
                                image_size=size_image,
                                n_threads=4,
                            )

            getpycomic.to_json()

        else:
            print(">")
            if isinstance(name, str):
                selected = getpycomic.build_Comic_from_path(path=name)
                if selected is None:
                    msg = f"\nThe given path `{name}` does not exist or does"
                    msg = msg + " not have images of the chapters.\n"
                    print(msg)
                    getpycomic.close_scraper()
                    return
            else:
                getpycomic.close_scraper()
                return

        if no_cbz is False:
            print("> Sorting volumes and chapters")
            getpycomic.sorter_by_volumes(
                comic=selected,
                chapters_by_volume=None,
                volumes_dict_chapters=matrix_dict["matrix"]
            )

            if debug:
                print(">> Volumes: ", selected.volumes)

            print("> Creating CBZ files.")
            getpycomic.to_cbz(
                            comic=selected,
                            preserve_images=no_preserve
                        )

            print("\n> Stored in directory: ", selected.path)

    except KeyboardInterrupt:
        if getpycomic is not None:
            getpycomic.to_json()
            getpycomic.close_scraper()


if __name__ == '__main__':
    main()
