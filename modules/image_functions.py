import os
import pathlib
import random
from PIL import Image, ImageDraw, ImageFont

path = os.path.dirname(os.path.realpath(__file__))


class Edit:
    """image creation and editing functions"""

    def __init__(self, image_location=path, save_location=path, font_location=path):
        self.folder = image_location
        self.temp = save_location
        self.fontPath = font_location

    def addText(self, imageName, fontSize, textColor, imagedict, new, fontName):
        """adds text to an image"""
        image = f"{self.folder}/{imageName}"
        edited = f"{self.temp}/{new}"

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

        for img in imagedict:
            draw.text(
                xy=(img[0][0], img[0][1]),
                text=img[1],
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

