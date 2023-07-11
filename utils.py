import math
import tkinter as tk
from functools import cache
from typing import Literal, Tuple, TypeVar

import PIL.Image
import numpy as np
from PIL import Image
from PIL import ImageTk

from logic.vector import Vector2

C = TypeVar("C")


def __force_cache(path: str, height: int | None = None, width: int | None = None):
    for flip_h in [True, False]:
        for flip_v in [True, False]:
            for degree in range(360):
                __load_image(path, height, width, flip_h, flip_v, degree)


def load_image(path: str, height: int | None = None, width: int | None = None,
               flip_h: bool = False, flip_v: bool = False,
               rotate: int = 0, pivot: Tuple[int, int] | None = None) -> Image:
    """
    Load an image from specified path and resize to specified _size, if any.
    Use cached image if available.
    If neither width nor height is provided, image is not resized.
    If either width or height is provided, the image is resized to specified dimension
    while scaling the other to keep aspect ratio.
    If both width and height are provided, image is resized to specified _size, aspect ratio is ignored.
    :param path: Relative path to image
    :param height: Target height in pixels to resize to, or None.
    :param width: Target width in pixels to resize to, or None.
    :param flip_h: Whether to _flip image horizontally.
    :param flip_v: Whether to _flip image vertically.
    :param rotate: What angle to rotate counter-clockwise by in degrees.
    :param pivot: Pivot point around which to rotate image in form of tuple (x,y)
    where (0,0) is the top left corner of image.
    :return: A PIL.Image loaded from specified path and processed according to args.
    """



    if rotate < 0:
        rotate = rotate + (360 * math.ceil(-rotate / 360))
    rotate %= 360
    rotate = math.floor(rotate)

    return __load_image(path=path, height=height, width=width,
                        flip_h=flip_h, flip_v=flip_v,
                        rotate=rotate, pivot=pivot)


@cache
def __load_image(path: str, height: int | None = None, width: int | None = None,
                 flip_h: bool = False, flip_v: bool = False,
                 rotate: int = 0, pivot: Tuple[int, int] | None = None) -> Image:
    assert rotate >= 0
    assert rotate < 360
    assert rotate % 1 == 0

    with Image.open(path) as image:
        if height is not None or width is not None:
            if height is None:
                aspect = width / image.width
                height = int(aspect * image.height)
            elif width is None:
                aspect = height / image.height
                width = int(aspect * image.width)
            image = image.resize(size=(width, height))
        else:
            # lazy reading may cause image not being loaded, resizing forces it
            image.load()

        if flip_h:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)

        if flip_v:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

        if rotate != 0:
            image = image.rotate(rotate, expand=True, center=pivot)

        return image


def load_photo(path: str, height: int | None = None, width: int | None = None,
               flip_h: bool = False, flip_v: bool = False,
               rotate: int = 0, pivot: Tuple[int, int] | None = None) -> tk.PhotoImage:
    """
    Load an image as PhotoImage from specified path and resize to specified _size, if any.
    Use cached image if available.
    If neither width nor height is provided, image is not resized.
    If either width or height is provided, the image is resized to specified dimension
    while scaling the other to keep aspect ratio.
    If both width and height are provided, image is resized to specified _size, aspect ratio is ignored.
    :param path: Relative path to image
    :param height: Target height in pixels to resize to, or None.
    :param width: Target width in pixels to resize to, or None.
    :param flip_h: Whether to _flip image horizontally.
    :param flip_v: Whether to _flip image vertically.
    :param rotate: What angle to rotate counter-clockwise by in degrees.
    :param pivot: Pivot point around which to rotate image in form of tuple (x,y)
    where (0,0) is the top left corner of image.
    :return: A tk.PhotoImage loaded from specified path and processed according to args.
    """
    if rotate < 0:
        rotate = rotate + (360 * math.ceil(-rotate / 360))
    rotate %= 360
    rotate = math.floor(rotate)

    return __load_photo(path=path, height=height, width=width,
                        flip_h=flip_h, flip_v=flip_v,
                        rotate=rotate, pivot=pivot)


@cache
def __load_photo(path: str, height: int | None = None, width: int | None = None,
                 flip_h: bool = False, flip_v: bool = False,
                 rotate: int = 0, pivot: Tuple[int, int] | None = None) -> tk.PhotoImage:
    image = load_image(path, height, width, flip_h, flip_v, rotate, pivot)
    photo = ImageTk.PhotoImage(image)
    return photo


def as_image(image: np.ndarray, mode: Literal["L", "RGB", "RGBA"] = None) -> PIL.Image.Image:
    """
    Convert numpy ndarray into a PIL.Image
    :param image: Ndarray to convert to image
    :param mode: One of 'L' (grayscale), 'RGB', 'RGBA'
    :return: tk.PhotoImage containing provided image as ndarray.
    """
    if mode is None:
        if image.ndim == 2:
            print("to image gray")
            return Image.fromarray(image.astype(np.uint8), mode="L")
        elif image.ndim == 3 and image.shape[2] == 3:
            print("to image rgb")
            return Image.fromarray(image.astype(np.uint8), mode="RGB")
        elif image.ndim == 3 and image.shape[2] == 4:
            print("to image rgba")
            return Image.fromarray(image.astype(np.uint8), mode="RGBA")
        else:
            raise ValueError(
                f"Unexpected image of shape {image.shape}, should be either 2D, or 3D with last dim of _size 3 or 4")
    else:
        return Image.fromarray(image.astype(np.uint8), mode=mode)


def as_photo(image: np.ndarray, mode: Literal["L", "RGB", "RGBA"] = None) -> tk.PhotoImage:
    """
    Convert numpy ndarray into a tk.PhotoImage
    :param image: Ndarray to convert to image
    :param mode: One of 'L' (grayscale), 'RGB', 'RGBA'
    :return: tk.PhotoImage containing provided image as ndarray.
    """

    if mode is None:
        if image.ndim == 2:
            print("to image gray")
            return ImageTk.PhotoImage(image=Image.fromarray(image.astype(np.uint8), mode="L"))
        elif image.ndim == 3 and image.shape[2] == 3:
            print("to image rgb")
            return ImageTk.PhotoImage(image=Image.fromarray(image.astype(np.uint8), mode="RGB"))
        elif image.ndim == 3 and image.shape[2] == 4:
            print("to image rgba")
            return ImageTk.PhotoImage(image=Image.fromarray(image.astype(np.uint8), mode="RGBA"))
        else:
            raise ValueError(
                f"Unexpected image of shape {image.shape}, should be either 2D, or 3D with last dim of _size 3 or 4")
    else:
        return ImageTk.PhotoImage(image=Image.fromarray(image.astype(np.uint8), mode=mode))


def rotate_vec(vector: Vector2, angle: float) -> (float, float):
    """
    Rotate a vector clockwise by a specified angle in degrees
    :param vector: Tuple in form (x,y) specifying a vector
    :param angle: Angle in degrees by which to rotate the vector in clockwise direction.
    :return: Tuple in form (x,y) specifying a rotated vector
    """
    radians = math.radians(angle)
    return Vector2(
        vector.x * math.cos(radians) - vector.y * math.sin(radians),
        vector.x * math.sin(radians) + vector.y * math.cos(radians)
    )


def clamp(value: C, bot: C, top: C) -> C:
    if bot > top:
        return clamp(value, top, bot)
    return min(top, max(bot, value))
