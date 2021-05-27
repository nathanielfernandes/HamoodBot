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
        self.ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "][
            ::-1
        ]

        if image:
            self.image = image
        elif image_location:
            self.image = self.open_image(image_location)
        elif image_url:
            self.image = self.download_image(image_url)

        if self.image.format == "GIF":
            self.image.seek(0)
            self.enhance_image()

    def __len__(self):
        return 1

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

    def get_image_bytes(
        self,
        image=None,
        file_name=None,
        location=None,
        file_format="png",
        size=None,
        compression_level=None,
        optimize=True,
    ):
        if image is None:
            image = self.image
            image = image.convert("RGB")

        if size is not None:
            image.resize(size)

        img_byte_arr = BytesIO()

        if compression_level is not None:
            image.save(
                img_byte_arr,
                format="JPEG",
                optimize=optimize,
                quality=compression_level,
            )
        else:
            image.save(img_byte_arr, format="png")
        img_byte_arr.seek(0),
        return img_byte_arr, "png"

    def save_image(
        self,
        image=None,
        file_name=None,
        location=None,
        file_format="jpg",
        size=None,
        compression_level=None,
        optimize=True,
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
                optimize=optimize,
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

    def regulate_size(self, image=None, scale=100):
        if image is None:
            image = self.image

        w, h = image.size
        r = h / w
        height_f = int(scale * r)
        resized_image = image.resize((int(scale * 1.75), height_f))

        self.image = resized_image
        return self.image

    def image_grayscale(self, image=None):
        if image is None:
            image = self.image
        g_image = image.convert("L")
        self.image = g_image
        return self.image

    def image_to_ascii(self, image=None, scale=None):
        if image is None:
            image = self.image

        if scale is None:
            scale = image.size[0]

        pixels = image.getdata()

        ascii_pixels = "".join([self.ASCII_CHARS[p // 25] for p in pixels])
        return "\n".join(
            ascii_pixels[i : (i + scale)] for i in range(0, len(ascii_pixels), scale)
        )


class Modify_Gif(Modify):
    def __init__(self, gif=None, gif_location=None, gif_url=None):
        """
        gif: PIL gif (or image)\n
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

        if self.gif.format != "GIF":
            self.duration = 5.0
            self.gif = [self.gif for f in range(10)]
        else:
            self.duration = self.gif.info.get("duration")
            if self.duration is None:
                self.duration = 5.0
            self.gif = [f.convert("RGBA") for f in ImageSequence.Iterator(self.gif)]

    def __len__(self):
        return len(self.gif)

    def get_gif_bytes(
        self,
        gif=None,
        file_name=None,
        location=None,
        optimize=False,
        compression_level=None,
    ):
        if gif is None:
            gif = self.gif

        gif_byte_arr = BytesIO()
        self.gif[0].save(
            gif_byte_arr,
            format="GIF",
            save_all=True,
            optimize=optimize,
            append_images=self.gif[1:],
            loop=False,
            duration=self.duration,  # self.og_gif.info["duration"],
        )
        gif_byte_arr.seek(0)
        return gif_byte_arr, "gif"

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
            duration=self.duration,  # self.og_gif.info["duration"],
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
        return self.gif

    def image_add_gif(
        self,
        base_image=None,
        top_gif=None,
        coordinates=(0, 0),
        top_gif_size=None,
        top_gif_rotation=None,
    ):
        if base_image is None:
            base_image = self.image
        if top_gif is None:
            top_gif = self.gif

        base_image = [copy(base_image) for f in range(len(top_gif))]

        self.gif = [
            self.image_add_image(
                base_image[i], top_gif[i], coordinates, top_gif_size, top_gif_rotation
            )
            for i in range(len(top_gif))
        ]

        return self.gif


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


def makeColorImg(rgba, path, size=(100, 100)):
    img = Image.new("RGBA", size, color=tuple(rgba))
    img_name = path + "".join(random.choice("123456789") for i in range(12)) + ".png"
    img.save(img_name)
    return img_name


def randomFile(folder):
    """selects a random file from a folder"""
    card = f"{folder}/{random.choice(os.listdir(folder))}"
    return card


def sussify(image: Image, scale: int = 20):
    gif = False

    default = image

    size = default.image.size

    sx, sy, = scale * round(size[0] / scale), scale * round(size[1] / scale)

    amogus = Modify_Gif(gif_location="modules/frames/amogusnbg.gif")
    amogus.resize_gif(size=(scale, scale))
    amogus_frames = []

    for frame in amogus.gif:
        frame = frame.convert("RGBA")
        amogus_frames.append(frame)

    amogus1 = [
        Modify(image_location=f"modules/frames/f{i}.png").resize_image(
            size=(scale, scale)
        )
        for i in range(6)
    ]
    amogus_frames1 = [frame.convert("RGBA") for frame in amogus1]

    if gif:
        default.resize_gif(size=(round(sx / scale), round(sy / scale)))
    else:
        default.image = default.image.convert("RGBA")
        default.resize_image(size=(round(sx / scale), round(sy / scale)))
        default.duration = 80
        default.gif = [default.image.copy() for _ in range(6)]

    color_pixels = [list(frame.getdata()) for frame in default.gif]

    fc = 0
    size = default.image.size

    def incr_fc(fc):
        fc += 1
        if fc >= len(amogus_frames):
            fc = 0

    def get_frame(fc):
        frame = (amogus_frames[fc], amogus_frames1[fc])
        incr_fc(fc)
        return frame

    final_frames = []

    start = 0
    blank = Image.new("RGBA", (sx, sy), (0, 0, 0, 255))
    for pixel_frame in color_pixels:
        if start < 6:
            fc = start
        else:
            start = 0
        curr_frame = blank.copy()

        x, y = 0, 0
        for color in pixel_frame:
            amg, amg1 = get_frame(fc)

            color_pixel = Image.new("RGBA", (scale, scale), color,)
            color_pixel.paste(amg1, (0, 0), amg1)
            curr_frame.paste(color_pixel, (x, y), amg)
            x += scale

            if x == sx:
                incr_fc(fc)
                x = 0
                y += scale
                skip = True
        start += 1
        final_frames.append(curr_frame)

    savename = f'temp/{"".join(random.choice("123456789") for i in range(12))}.gif'
    final_frames[0].save(
        savename,
        format="GIF",
        save_all=True,
        optimize=False,
        append_images=final_frames[1:],
        loop=False,
        duration=default.duration,
    )

    return savename


# from progress.bar import Bar

# # typ = input("img/gif: ")


# link = input("Link: ")

# gif = ".gif" in link

# print("--GRABBING IMAGE--")

# if gif:
#     default = Modify_Gif(gif_url=link)
# else:
#     default = Modify(image_url=link)

# size = default.image.size
# print("--IMAGE READY--\n")
# print(f"Resolution: {size[0]}x{size[1]}\n")


# while True:
#     scale = int(input("Enter Susxle Size (px): "))
#     sx, sy, = scale * round(size[0] / scale), scale * round(size[1] / scale)

#     print(f"Final Resolution: {sx}x{sy}\n")

#     con = input("Continue? (y/n): ")

#     if con == "y":
#         break

#     print("")


# amogus = Modify_Gif(gif_location="/Users/nathaniel/Desktop/amogusnbg.gif")
# amogus.resize_gif(size=(scale, scale))
# amogus_frames = []


# for frame in amogus.gif:
#     frame = frame.convert("RGBA")
#     amogus_frames.append(frame)


# amogus1 = [
#     Modify(
#         image_location=f"/Users/nathaniel/Desktop/HamoodBot/modules/frames/f{i}.png"
#     ).resize_image(size=(scale, scale))
#     for i in range(6)
# ]
# amogus_frames1 = [frame.convert("RGBA") for frame in amogus1]


# if gif:
#     default.resize_gif(size=(round(sx / scale), round(sy / scale)))
# else:
#     default.image = default.image.convert("RGBA")
#     default.resize_image(size=(round(sx / scale), round(sy / scale)))
#     default.duration = 80
#     default.gif = [default.image.copy() for _ in range(6)]


# print("--STARTING--\n")

# color_pixels = [list(frame.getdata()) for frame in default.gif]

# bar = Bar(
#     "Sussifying",
#     max=len(color_pixels) * len(color_pixels[0]),
#     suffix="%(percent).1f%% \t Susxle: %(index)d/%(max)d",
#     fill="#",
# )

# fc = 0
# size = default.image.size


# def incr_fc():
#     global fc
#     fc += 1
#     if fc >= len(amogus_frames):
#         fc = 0


# def get_frame():
#     frame = (amogus_frames[fc], amogus_frames1[fc])
#     incr_fc()
#     return frame


# final_frames = []

# start = 0
# blank = Image.new("RGBA", (sx, sy), (0, 0, 0, 255))
# for pixel_frame in color_pixels:
#     if start < 6:
#         fc = start
#     else:
#         start = 0
#     curr_frame = blank.copy()

#     x, y = 0, 0
#     for color in pixel_frame:
#         amg, amg1 = get_frame()

#         color_pixel = Image.new("RGBA", (scale, scale), color,)
#         color_pixel.paste(amg1, (0, 0), amg1)
#         curr_frame.paste(color_pixel, (x, y), amg)
#         x += scale
#         bar.next()
#         if x == sx:
#             incr_fc()
#             x = 0
#             y += scale
#             skip = True
#     start += 1
#     final_frames.append(curr_frame)

# bar.finish()
# print()
# print("--SAVING--")

# final_frames[0].save(
#     "test.gif",
#     format="GIF",
#     save_all=True,
#     optimize=False,
#     append_images=final_frames[1:],
#     loop=False,
#     duration=default.duration,
# )

# print("--DONE--")
