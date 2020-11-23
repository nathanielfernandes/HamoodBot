import os
import pathlib
import random
import io
from copy import copy
from PIL import Image, ImageDraw, ImageFont, ImageSequence, ImageEnhance

import requests
from io import BytesIO

path = os.path.dirname(os.path.realpath(__file__))


class Modify:
    """
    Methods to mutate and edit an Image
    """

    def __init__(self, image=None, image_location=None, image_url=None):
        """
        image: PIL img\n
        image_location: image name or path to image\n
        image_url: url of the image
        """
        self.image = None
        self.font = None

        if image:
            self.image = image
        elif image_location:
            self.image = self.open_image(image_location)
        elif image_url:
            self.image = self.download_image(image_url)

        if self.image.format == "GIF":
            self.image.seek(0)
            self.enhance_image()

    def open_image(self, image):
        """
        image: image name or location\n

        returns (optional): PIL PNG image
        """
        try:
            image = Image.open(image)
        except OSError as e:
            return e

        return image

    def download_image(self, url):
        """
        url: url of image (PNG, JPEG, JPG, GIF)\n

        returns: raw image data
        """
        try:
            response = requests.get(url)
        except Exception as e:
            return e

        return self.open_image(BytesIO(response.content))

    def set_font(self, font_location, font_size):
        """
        font_location: path to a font
        fot_size: font size to be used

        returns: PIL font
        """
        try:
            self.font = ImageFont.truetype(font_location, font_size)
        except Exception as e:
            return e

        return self.font

    def save_image(
        self,
        image=None,
        file_name=None,
        location=None,
        file_format="jpg",
        size=None,
        compression_level=None,
    ):
        """
        image: PIL image\n
        file_name: name of to be saved file\n
        location: where to save the new file\n
        file_format: format to save file in\n
        size: size to resize image to\n
        compression_level: amount of compression to be added
        """

        if image is None:
            image = self.image
            image = image.convert("RGB")

        if size is not None:
            image.resize(size)

        if file_name is None:
            file_name = (
                "".join(random.choice("123456789") for i in range(12))
                + "."
                + file_format.lower()
            )

        if location is None:
            location = ""
        elif location[-1] != "/":
            location += "/"

        if compression_level is not None:
            image.save(
                f"{location}{file_name}",
                "JPEG",
                optimize=True,
                quality=compression_level,
            )
        else:
            image.save(f"{location}{file_name}")

        return f"{location}{file_name}"

    def image_add_text(
        self,
        image=None,
        text="test",
        coordinates=(0, 0),
        font=None,
        font_color=(0, 0, 0),
        stroke_color=None,
        stroke_width=0,
    ):
        """
        image: PIL image\n
        text: text to be used\n
        coordinates: (x, y)position to place text\n
        font: PIL loaded font\n
        font_color: (r,g,b)\n
        stroke_color: (r,g,b)\n
        stroke_width: thickness of stroke
        """

        if image is None:
            image = self.image

        if font is None:
            font = self.font

        if stroke_color is None:
            r, g, b = font_color
            stroke_color = (255 - r, 255 - g, 255 - b)

        draw = ImageDraw.Draw(image)
        draw.text(
            xy=coordinates,
            text=text,
            fill=font_color,
            font=font,
            spacing=4,
            align="center",
            stroke_width=stroke_width,
            stroke_fill=stroke_color,
        )

        self.image = image
        return self.image

    def image_add_image(
        self,
        base_image=None,
        top_image=None,
        coordinates=(0, 0),
        top_image_size=None,
        top_image_rotation=None,
    ):
        """
            base_image: PIL image\n
            top_image: PIL image\n
            coordinates: (x, y) position to place image\n
            top_image_size: (x, y) size of image to place\n
            top_image_rotation: int, degrees of rotation
        """
        if base_image is None:
            base_image = self.image
        if top_image is None:
            top_image = self.image
        if top_image_size is not None:
            top_image = top_image.resize(top_image_size)

        top_image = top_image.convert("RGBA")
        base_image = base_image.convert("RGBA")
        # top_image.putalpha(255)

        if top_image_rotation is not None:
            top_image = top_image.rotate(top_image_rotation, expand=1).resize(
                top_image_size
            )

        base_image.paste(top_image, coordinates, top_image)

        self.image = base_image
        return self.image

    def enhance_image(
        self, image=None, sharpness=1.0, contrast=1.0, color=1.0, brightness=1.0
    ):
        """
            image: PIL Image\n
            sharpness: int, 1 being default\n
            contrast: int, 1 being default\n
            color: int, 1 being default\n
            brightness: int, 1 being default
        """
        if image is None:
            image = self.image

        if image.format == "PNG" or image.format == "GIF":
            image = image.convert("RGB")

        image = ImageEnhance.Sharpness(image).enhance(sharpness)
        image = ImageEnhance.Contrast(image).enhance(contrast)
        image = ImageEnhance.Color(image).enhance(color)
        image = ImageEnhance.Brightness(image).enhance(brightness)

        self.image = image
        return self.image

    def resize_image(self, image=None, size=(64, 64), constant_resolution=False):
        if image is None:
            image = self.image

        resized = image.resize(size, resample=Image.BILINEAR)

        if constant_resolution:
            resized = resized.resize(image.size, Image.NEAREST)

        self.image = resized
        return self.image


class Modify_Gif(Modify):
    def __init__(self, gif=None, gif_location=None, gif_url=None):
        """
        gif: PIL gif\n
        gif_location: gif name or path to gif\n
        gif_url: url of the gif
        """
        super().__init__(image=gif, image_location=gif_location, image_url=gif_url)
        # self.gif_resize_image = self.resize_image

        self.set_font = self.set_font
        # self.gif = None

        if gif:
            self.gif = gif
        elif gif_location:
            self.gif = self.open_image(gif_location)
        elif gif_url:
            self.gif = self.download_image(gif_url)

        self.og_gif = copy(self.gif)

        self.gif = [f.convert("RGBA") for f in ImageSequence.Iterator(self.gif)]

    def save_gif(
        self,
        gif=None,
        file_name=None,
        location=None,
        optimize=False,
        compression_level=None,
    ):
        if gif is None:
            gif = self.gif

        if file_name is None:
            file_name = "".join(random.choice("123456789") for i in range(12)) + ".gif"

        if location is None:
            location = ""
        elif location[-1] != "/":
            location += "/"

        # frames = [f.convert("RGBA") for f in ImageSequence.Iterator(gif)]
        gif[0].save(
            f"{location}{file_name}",
            format="GIF",
            save_all=True,
            optimize=optimize,
            append_images=gif[1:],
            loop=False,
            duration=self.og_gif.info["duration"],
        )

        return f"{location}{file_name}"

    def gif_add_text(
        self,
        gif=None,
        text="test",
        coordinates=(0, 0),
        font=None,
        font_color=(255, 255, 255),
        stroke_color=None,
        stroke_width=0,
    ):
        if gif is None:
            gif = self.gif

        if font is None:
            font = self.font

        if stroke_color is None:
            r, g, b = font_color
            stroke_color = (255 - r, 255 - g, 255 - b)

        frames = []
        for f in gif:
            draw = ImageDraw.Draw(f)
            draw.text(
                xy=coordinates,
                text=text,
                fill=font_color,
                font=font,
                spacing=4,
                align="center",
                stroke_width=stroke_width,
                stroke_fill=stroke_color,
            )
            del draw
            frames.append(f)
        self.gifs = frames
        return self.gifs

    def enhance_gif(
        self, gif=None, sharpness=1.0, contrast=1.0, color=1.0, brightness=1.0
    ):
        if gif is None:
            gif = self.gif

        self.gif = [
            self.enhance_image(f, sharpness, contrast, color, brightness) for f in gif
        ]

        return self.gif

    def resize_gif(self, gif=None, size=(64, 64), constant_resolution=False):
        if gif is None:
            gif = self.gif

        self.gif = [self.resize_image(f, size, constant_resolution) for f in gif]

        return self.gif

    def gif_add_image(
        self,
        base_gif=None,
        top_image=None,
        coordinates=(0, 0),
        top_image_size=None,
        top_image_rotation=None,
    ):
        if base_gif is None:
            base_gif = self.gif
        if top_image is None:
            top_image = self.image
        if top_image_size is not None:
            top_image = top_image.resize(top_image_size)

        self.gif = [
            self.image_add_image(
                f, top_image, coordinates, top_image_size, top_image_rotation
            )
            for f in base_gif
        ]


# needs work
def makeText(content, font, font_size, colour, final):
    """turns text from text into an image of the text"""

    placeholderImg = Image.new("RGBA", (0, 0), (0, 0, 0, 0))

    fontType = ImageFont.truetype(font, font_size)

    placeholderDraw = ImageDraw.Draw(placeholderImg)

    text_size = placeholderDraw.textsize(content, fontType)

    img = Image.new("RGBA", (text_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text(
        xy=(0, 0),
        text=content,
        fill=colour,
        font=fontType,
        anchor=None,
        spacing=0,
        align="left",
    )

    img.save(final)
    return final


def randomFile(folder):
    """selects a random file from a folder"""
    card = f"{folder}/{random.choice(os.listdir(folder))}"
    return card
