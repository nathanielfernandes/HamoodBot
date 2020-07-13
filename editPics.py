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

    if textColor == 'BLACK':
        textColor = (0,0,0)
        STROKECOLOR = (255,255,255)
    elif textColor == 'WHITE':
        textColor = (255,255,255)
        STROKECOLOR = (0,0,0)

    for img in imagedict:
        if ('/' in img[1]):
            fontSize -= 5
        itext = img[1].replace('/', '\n')
        draw.text(xy=(img[0][0], img[0][1]), text=itext, fill=(textColor), font=font_type, anchor=None, spacing=4, align="center", direction=None, features=None, language=None, stroke_width=4, stroke_fill=STROKECOLOR)
        
    image.save(edited)
    return edited

def addImage(background, imageList, size, new):
    folder = path + '/' + "memePics"
    back = Image.open(folder + '/' + background)
    finalName = folder + '/' + new
    
    for img in imageList:
        front = Image.open(img[2])
        front = front.resize(size)
        front.putalpha(255)
        front = front.rotate(img[1], expand=1).resize(size)
        back.paste(front, (img[0]), front)
        
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
