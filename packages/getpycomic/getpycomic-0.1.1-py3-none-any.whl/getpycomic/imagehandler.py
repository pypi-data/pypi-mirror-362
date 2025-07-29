# -*- coding: utf-8 -*-
"""

Options for resize images.
* 'original' :  original size.
* 'small'     :  800 x 1200.
* 'medium'    :  1000 x 1500.
* 'large'     :  1200 x 1800.
"""

from PIL import Image
import io

from typing import (
        TypeVar,
        Union,
        Literal
    )

ImageInstancePIL = TypeVar("ImageInstancePIL")


class ImagesHandler:
    """
    Class dealing with image issues, such as resizing.
    """
    validFormats = {
        'JPEG': 'jpeg',
        'PNG': 'png',
        'JPG': 'jpg',
        'WEBP': 'webp',
    }
    sizeImageDict = {
        'original': None,
        'small': (800, 1200),
        'medium': (1000, 1500),
        'large': (1200, 1800),
    }

    @staticmethod
    def get_size(
        size: str = 'original'
    ) -> tuple:
        """
        Returns tuple of size.

        Args
            size: string indicating the new size of the image.

        Returns
            tuple: tuple of int.
        """
        try:
            return ImagesHandler.sizeImageDict[size]
        except KeyError:
            return ImagesHandler.sizeImageDict['small']

    @staticmethod
    def new_image(
        currentImage: bytes,
        extension: str = "jpeg",
        sizeImage: Literal["original", "small", "medium", "large"] = "original",
    ) -> io.BytesIO:
        """
        Resize image.

        Args:
            currentImage: bytes of image.
            extension: extension of new image.
            sizeImage: category of size to resize original image. Default is
                       'original'.

        Returns:

        """
        size_tuple = ImagesHandler.get_size(size=sizeImage)
        newImageIO = io.BytesIO()

        with Image.open(currentImage) as image_:
            # force image color, RGB.
            image_rbg = image_.convert('RGB')

            if size_tuple is not None:
                imageResized = image_rbg.resize(
                                        size_tuple,
                                        resample=Image.Resampling.LANCZOS
                                    )
            else:
                imageResized = image_rbg

            imageResized.save(
                    newImageIO,
                    format=extension,
                    quality=100
                )

        return newImageIO

    @staticmethod
    def save_image(
        path_image: str,
        image: Union[io.BytesIO, bytes]
    ) -> bool:
        """
        """
        try:
            with open(path_image, 'wb') as file:
                if isinstance(image, io.BytesIO):
                    file.write(image.getvalue())
                elif isinstance(image, bytes):
                    file.write(image)
                return True
        except Exception as e:
            print("Error: ImagesHandler", e)
            return False
