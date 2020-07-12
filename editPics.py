import os
import pathlib

import random
import requests
# import cv2

from PIL import Image, ImageDraw, ImageFont

# import requests

path = os.path.dirname(os.path.realpath(__file__))

def addText(imageName, fontSize, textColor, imagedict, new):
    folder = path + '/' + "memePics"
    image = folder + '/' + imageName
    edited = folder + '/' + new

    fontPath = folder + '/' + 'arialbold.ttf'

    image = Image.open(image)   
    font_type = ImageFont.truetype(fontPath, fontSize)
    draw = ImageDraw.Draw(image)

    if textColor[0] == 255:
        STROKECOLOR = (0,0,0)
    elif textColor[0] == 0:
        STROKECOLOR = (255,255,255)

    for img in imagedict:
        if ('/' in img[0]):
            fontSize -= 5
        itext = img[0].replace('/', '\n')
        draw.text(xy=(img[1][0], img[1][1]), text=itext, fill=(textColor), font=font_type, anchor=None, spacing=4, align="center", direction=None, features=None, language=None, stroke_width=4, stroke_fill=STROKECOLOR)
        
    image.save(edited)
    return edited

def addImage(background, imageList, size, new):
    folder = path + '/' + "memePics"
    back = Image.open(folder + '/' + background)
    finalName = folder + '/' + new
    
    for img in imageList:
        front = Image.open(img[0])
        front = front.resize(size)
        back.paste(front, (img[1]))

    back.save(finalName)
    return finalName

def scrape(imgURL, saveDir):
    img_data = requests.get(imgURL).content
    with open(saveDir, 'wb') as handler:
        handler.write(img_data)

def randomNumber():
    char = '1234567890'
    combo = ''
    for i in range(12):
        num = random.choice(char)
        combo += num
        
    return combo

def deleteImage(file):
    os.remove(file)
