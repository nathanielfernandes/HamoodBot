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
        font_color=(255, 255, 255),
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

    def add_image(
        self,
        base_image=None,
        top_image=None,
        coordinates=(0, 0),
        top_image_size=None,
        top_image_rotation=None,
    ):
        if base_image is None:
            base_image = self.image
        if top_image is None:
            top_image = self.image
        if top_image_size is not None:
            top_image = top_image.resize(top_image_size)

        top_image.putalpha(255)

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


### soon to be removed ###
class Edit:
    """image creation and editing functions"""

    def __init__(self, image_location=path, save_location=path, font_location=path):
        self.folder = image_location
        self.temp = save_location
        self.fontPath = font_location

    def deep_fry(self, imageName, newname, ext):
        """deepfries an image"""

        def fry(img):
            img = ImageEnhance.Sharpness(img).enhance(10000)
            img = ImageEnhance.Contrast(img).enhance(10000)
            img = ImageEnhance.Color(img).enhance(10000)
            img = ImageEnhance.Brightness(img).enhance(10000)

            return img

        img = f"{self.temp}/{imageName}"
        edited = f"{self.temp}/{newname}"

        img = Image.open(img)

        if ext == "gif":
            frames = []
            for frame in ImageSequence.Iterator(img):
                frames.append(fry(frame.convert("RGBA")))

            frames[0].save(
                edited,
                save_all=True,
                append_images=frames[1:],
                optimize=False,
                loop=False,
                duration=img.info["duration"],
            )
        else:
            if ext == "png":
                img = img.convert("RGB")

            img = fry(img)
            img.save(edited, "JPEG", optimize=True, quality=10)

        return edited

    def gif_rgb(self, gifName, newname):
        """makes a gif rgb"""

        gif = f"{self.temp}/{gifName}"
        edited = f"{self.temp}/{newname}"

        gif = Image.open(gif)

        frames = []
        for frame in ImageSequence.Iterator(gif):
            # frame = frame.convert("RGB")
            en = ImageEnhance.Contrast(gif)
            gif = en.enhance(200)

            frames.append(frame)
        frames[0].save(
            edited, format="GIF", save_all=True, append_images=frames[1:],
        )

    def gif_addText(self, gifName, fontSize, textColor, textData, newname, fontName):
        """adds text to a gif"""
        gif = f"{self.folder}/{gifName}"
        edited = f"{self.temp}/{newname}"

        fontLoc = f"{self.fontPath}/{fontName}"

        gif = Image.open(gif)
        font_type = ImageFont.truetype(fontLoc, fontSize)

        if textColor == "BLACK":
            textColor = (0, 0, 0)
            STROKECOLOR = (255, 255, 255)
        elif textColor == "WHITE":
            textColor = (255, 255, 255)
            STROKECOLOR = (0, 0, 0)

        frames = []
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")

            for key in textData:
                draw = ImageDraw.Draw(frame)
                draw.text(
                    xy=(textData[key][0], textData[key][1]),
                    text=key,
                    fill=(textColor),
                    font=font_type,
                    anchor=None,
                    spacing=4,
                    align="center",
                    direction=None,
                    features=None,
                    language=None,
                    stroke_width=4,
                    stroke_fill=STROKECOLOR,
                )
                del draw

            frames.append(frame)

            # my_bytes = io.BytesIO()
        frames[0].save(edited, format="GIF", save_all=True, append_images=frames[1:])
        # print(my_bytes.getvalue())
        return edited

    def addText(self, imageName, fontSize, textColor, textData, newname, fontName):
        """adds text to an image"""
        image = f"{self.folder}/{imageName}"
        edited = f"{self.temp}/{newname}"

        fontLoc = f"{self.fontPath}/{fontName}"

        image = Image.open(image)
        font_type = ImageFont.truetype(fontLoc, fontSize)
        draw = ImageDraw.Draw(image)

        if textColor == "BLACK":
            textColor = (0, 0, 0)
            STROKECOLOR = (255, 255, 255)
        elif textColor == "WHITE":
            textColor = (255, 255, 255)
            STROKECOLOR = (0, 0, 0)

        for key in textData:
            draw.text(
                xy=(textData[key][0], textData[key][1]),
                text=key,
                fill=(textColor),
                font=font_type,
                spacing=4,
                align="center",
                stroke_width=4,
                stroke_fill=STROKECOLOR,
            )

        image.save(edited)
        return edited

    def makeText(self, content, font, font_size, colour, final):
        """turns text from text into an image of the text"""
        fontLoc = f"{self.fontPath}/{font}"
        finalName = f"{self.temp}/{final}"

        placeholderImg = Image.new("RGBA", (0, 0), (0, 0, 0, 0))

        fontType = ImageFont.truetype(fontLoc, font_size)

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

        img.save(finalName)
        return finalName

    def addImage(self, background, imageList, size, new):
        """adds images on top of an image"""
        back = Image.open(f"{self.folder}/{background}")
        finalName = f"{self.temp}/{new}"

        for img in imageList:
            front = Image.open(img[2])
            front = front.resize(size)
            front.putalpha(255)
            front = front.rotate(img[1], expand=1).resize(size)
            back.paste(front, (img[0]), front)

        back.save(finalName)
        return finalName

    def randomFile(self, folder):
        """selects a random file from a folder"""
        card = f"{folder}/{random.choice(os.listdir(folder))}"
        return card

    def randomNumber(self):
        """generates a random string of numbers"""
        combo = ""
        for i in range(12):
            num = random.choice("1234567890")
            combo += num
        return combo
