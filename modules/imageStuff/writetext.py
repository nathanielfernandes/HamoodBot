"""
Requirement: PIL <http://www.pythonware.com/products/pil/>
Copyright 2011 Álvaro Justen [alvarojusten at gmail dot com]
License: GPL <http://www.gnu.org/copyleft/gpl.html>
With modifications by Nathaniel Fernandes (nathaniel.s.fernandes@gmail.com)
"""
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
import re

EMOJI = r"(<a?:\w+:?\d+>)"


class WriteText(object):
    def __init__(self, im: Image):
        self.image = im
        self.size = self.image.size

    # self.draw = ImageDraw.Draw(self.image)

    def ret_img(self):
        return self.image

    def get_font_size(self, text, font, max_width, max_height):
        if max_width is None and max_height is None:
            raise ValueError("You need to pass max_width or max_height")
        font_size = 1
        text_size = self.get_text_size(font, font_size, text)
        if (max_width is not None and text_size[0] > max_width) or (
            max_height is not None and text_size[1] > max_height
        ):
            raise ValueError("Text can't be filled in only (%dpx, %dpx)" % text_size)
        while True:
            if (max_width is not None and text_size[0] >= max_width) or (
                max_height is not None and text_size[1] >= max_height
            ):
                return font_size - 1
            font_size += 1
            text_size = self.get_text_size(font, font_size, text)

    def write_text(
        self,
        x,
        y,
        text,
        font_filename,
        font_size,
        max_width=None,
        max_height=None,
        color=(0, 0, 0),
    ):
        if font_size == "fill" and (max_width is not None or max_height is not None):
            font_size = self.get_font_size(text, font_filename, max_width, max_height)
        text_size = self.get_text_size(font_filename, font_size, text)
        font = ImageFont.truetype(font_filename, font_size)
        if x == "center":
            x = (self.size[0] - text_size[0]) / 2
        if y == "center":
            y = (self.size[1] - text_size[1]) / 2
        # self.draw.text((x, y), text, font=font, fill=color)
        with Pilmoji(self.image) as pilmoji:
            pilmoji.text(
                xy=(round(x), round(y)),
                text=text,
                font=font,
                fill=color,
                emoji_size_factor=1,
                emoji_position_offset=(0, 6),
            )

        return text_size

    @staticmethod
    def get_text_size(font_filename, font_size, text):
        font = ImageFont.truetype(font_filename, font_size)
        return font.getsize(re.sub(EMOJI, "O", text))

    def write_text_box(
        self,
        x,
        y,
        text,
        box_width,
        font_filename,
        font_size,
        color,
        place="left",
        justify_last_line=False,
    ):
        lines = []
        line = []
        words = text.split()
        for word in words:
            new_line = " ".join(line + [word])
            size = self.get_text_size(font_filename, font_size, new_line)
            text_height = size[1]
            if size[0] <= box_width:
                line.append(word)
            else:
                lines.append(line)
                line = [word]
        if line:
            lines.append(line)
        lines = [" ".join(line) for line in lines if line]
        height = y
        for index, line in enumerate(lines):
            height += text_height
            if place == "left":
                self.write_text(x, height, line, font_filename, font_size, color=color)
            elif place == "right":
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = x + box_width - total_size[0]
                self.write_text(
                    x_left, height, line, font_filename, font_size, color=color
                )
            elif place == "center":
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = int(x + ((box_width - total_size[0]) / 2))
                self.write_text(
                    x_left, height, line, font_filename, font_size, color=color
                )
            elif place == "justify":
                words = line.split()
                if (index == len(lines) - 1 and not justify_last_line) or len(
                    words
                ) == 1:
                    self.write_text(
                        x, height, line, font_filename, font_size, color=color
                    )
                    continue
                line_without_spaces = "".join(words)
                total_size = self.get_text_size(
                    font_filename, font_size, line_without_spaces
                )
                space_width = (box_width - total_size[0]) / (len(words) - 1.0)
                start_x = x
                for word in words[:-1]:
                    self.write_text(
                        start_x, height, word, font_filename, font_size, color=color
                    )
                    word_size = self.get_text_size(font_filename, font_size, word)
                    start_x += word_size[0] + space_width
                last_word_size = self.get_text_size(font_filename, font_size, words[-1])
                last_word_x = x + box_width - last_word_size[0]

                self.write_text(
                    last_word_x,
                    height,
                    words[-1],
                    font_filename,
                    font_size,
                    color=color,
                )
        fsizee = self.get_text_size(font_filename, font_size, "text")
        height += int(fsizee[1] * 1.5)
        return height
