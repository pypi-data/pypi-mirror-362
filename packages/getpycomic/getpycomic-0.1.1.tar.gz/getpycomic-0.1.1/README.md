# getpycomic

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Searches and obtains the manga/comic images and generates a *CBZ* file. Allows to group the chapters by volumes.

By default, it uses 6 chapters per volume or if you want to know the volumes and chapters you can consult that information at [https://comick.io](https://comick.io).

It also allows to convert directories with manga/comic images into CBZ files. Internal directory structure you must have:

```bash
DIRECTORY
├── 1.0
│   ├── 001.jpg
│   ├── 002.jpg
│   └── 003.jpg
├── 2.0
│   ├── 001.jpg
│   ├── 002.jpg
│   └── 003.jpg
└── 3.0
    ├── 001.jpg
    ├── 002.jpg
    └── 003.jpg
```

All images and CBZ files are stored on the current user's desktop.

## Supported pages

- [tmomanga](https://tmomanga.com/)
- [zonatmo](https://zonatmo.com/)
- [novelcool](https://novelcool.com/)

To request new pages, make a new `issue` with `enhancement` tag.

<br>

> [!NOTE]
> This project aims to give you the possibility to take this entertainment wherever you go, even without an Internet connection.

> [!IMPORTANT]
> You must have [Firefox](https://www.mozilla.org/) installed.
It will search the default paths of *Firefox*. If it is not found or installed in another path, use the `--firefox-bin` argument and the full path to the executable.

> [!IMPORTANT]
> **DISCLAIMER:**  
> This application does not host, distribute, or store any copyrighted content.
> It is a technical tool intended for personal or educational purposes only.
> The author is not responsible for any misuse or legal consequences resulting from its use.


<br>

# Installation

```bash
$ pip install getpycomic
```


# Usage

```bash
$ getpycomic --help
usage: getpycomic [-h] -n NAME_OR_PATH [NAME_OR_PATH ...] [-w {tmomanga,zonatmo,novelcool}] [-c CHAPTER] [-v VOLUMES [VOLUMES ...]] [--no-cbz]
                  [-e {selenium}] [-l {en,es,br,it,ru,de,fr}] [--no-download] [-s] [--verbose] [-i] [--debug] [--no-preserve]
                  [--size {original,small,medium,large}] [--firefox-bin FIREFOX_BIN]

Gets manga/comic from web to CBZ files.

optional arguments:
  -h, --help            show this help message and exit
  -n NAME_OR_PATH [NAME_OR_PATH ...], --name_or_path NAME_OR_PATH [NAME_OR_PATH ...]
                        Name of the manga/comic or path of the manga/comic downloaded
  -w {tmomanga,zonatmo,novelcool}, --web {tmomanga,zonatmo,novelcool}
                        Select website. Default `tmomanga`
  -c CHAPTER, --chapter CHAPTER
                        Chapters: `all`, `1,5`, `5+` `1-5`. Default `all`.
  -v VOLUMES [VOLUMES ...], --volumes VOLUMES [VOLUMES ...]
                        Indicate how the chapters will be put together by volume in the CBZ file. By default, each volume has `6` chapters. For
                        example: 1:[1,4],2:[5,9]
  --no-cbz              It only downloads chapters and does not create CBZ files.
  -e {selenium}, --engine {selenium}
                        Select engine to get data. Default `selenium`.
  -l {en,es,br,it,ru,de,fr}, --language {en,es,br,it,ru,de,fr}
                        Select language. Default `es`.
  --no-download         It does not configure the motor and does not prepare it.
  -s, --show            Show engine or not. Default is no.
  --verbose             Displays messages of all operations.
  -i, --interactive     Interactive Prompt for manga/comics search. By default the first item found is used.
  --debug               Show more messages for debug.
  --no-preserve         Preserve or not the manga/comic images. By default the images are preserved.
  --size {original,small,medium,large}
                        Select the size of the image. Default is `original`.
   FIREFOX_BIN
                        Binary path of Firefox.

You can read your manga/comics wherever you want.
```

## Image sizes

Available options used by the `--size` argument:

| Options | Sizes |
|-|-|
| `original` | retains original sizes |
| `small` | 800x1200 |
| `medium` | 1000x1500 |
| `large` | 1200x1800 |


# Examples

* gets all chapters and create volumes with 6 chapter.

```bash
$ getpycomic --name_or_path MANGA_NAME --web zonatmo
```

* gets all available chapters of "MANGA_NAME" from "zonatmo", all images are stored with `small` size and builds CBZ files with specific chapters.

```bash
$ getpycomic --name_or_path MANGA_NAME --web zonatmo --chapter all --size small --volumes 1: [1, 15],2: [16, 30],3: [31, 45]
```
or
```bash
$ getpycomic --name_or_path MANGA_NAME --web zonatmo --chapter all --size small --volumes 1:[1,15],2:[16,30],3:[31,45]
```

* convert image directory to CBZ files. Using `--volumes` you can specify chapters per volume, if omitted, 6 chapters per volume will be used.

```bash
$ getpycomic --name_or_path /path/DIRECTORY --no-download
```
or
```bash
$ getpycomic --name_or_path /path/DIRECTORY --no-download --volumes 1:[1,3]
```

* Pass the *Firefox* binary path.

Linux
```bash
$ getpycomic --name_or_path MANGA_NAME --firefox-bin /path/firefox
```

Windows

```bash
$ getpycomic --name_or_path MANGA_NAME --firefox-bin \path\firefox.exe
```


# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
