import os
import pathlib
import random
import messageFeatures
from PIL import Image, ImageDraw, ImageFont


# import requests
path = os.path.dirname(os.path.realpath(__file__))
folder = path + '/' + "memePics"
fontPath = path + '/' + 'fonts' + '/'

temp = path + '/' + 'tempImages' 

def addText(imageName, fontSize, textColor, imagedict, new):
    image = folder + '/' + imageName
    edited = temp + '/' + new

    f = getFont('arial')
    fontLoc = fontPath + f#'arialbold.ttf'

    image = Image.open(image)   
    font_type = ImageFont.truetype(fontLoc, fontSize)
    draw = ImageDraw.Draw(image)

    if textColor == 'BLACK':
        textColor = (0,0,0)
        STROKECOLOR = (255,255,255)
    elif textColor == 'WHITE':
        textColor = (255,255,255)
        STROKECOLOR = (0,0,0)

    for img in imagedict:
        draw.text(xy=(img[0][0], img[0][1]), text=img[1], fill=(textColor), font=font_type, anchor=None, spacing=4, align="center", direction=None, features=None, language=None, stroke_width=4, stroke_fill=STROKECOLOR)
        
    image.save(edited)
    return edited

def makeText(content, font, font_size, colour, final):
    fontLoc = fontPath + font
    finalName = path + '/' + 'tempImages' + '/' + final

    placeholderImg = Image.new('RGBA', (0, 0), (0, 0, 0, 0))

    fontType = ImageFont.truetype(fontLoc, font_size)

    placeholderDraw = ImageDraw.Draw(placeholderImg)

    text_size = placeholderDraw.textsize(content, fontType)

    img = Image.new('RGBA', (text_size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.text(xy=(0,0), text=content, fill=colour, font=fontType, anchor=None, spacing=0, align="left")

    img.save(finalName)
    return finalName

def addImage(background, imageList, size, new):
    back = Image.open(folder + '/' + background)
    finalName = temp + '/' + new
    
    for img in imageList:
        front = Image.open(img[2])
        front = front.resize(size)
        front.putalpha(255)
        front = front.rotate(img[1], expand=1).resize(size)
        back.paste(front, (img[0]), front)
        
    back.save(finalName)
    return finalName

def unoCard():
    path = os.path.dirname(os.path.realpath(__file__))
    folder = path + '/' + "unoCards"
    
    mix = random.randint(0,3)
    card = os.listdir(folder)
    card = folder + '/' + card[mix]
    return card

def randomNumber():
    char = '1234567890'
    combo = ''
    for i in range(12):
        num = random.choice(char)
        combo += num
        
    return combo

def deleteImage(file):
    os.remove(file)

def getFont(name):
    path = os.path.dirname(os.path.realpath(__file__))
    file = path + '/' + 'textFiles' + '/' + "fonts.txt"

    fontDict = messageFeatures.convert_to_dict(file)

    if name == 'random':
        font = random.choice(list(fontDict.values()))
    elif name not in fontDict:
        font = name
    else:
        font = fontDict[name]

    return font

def getColour(name):
    path = os.path.dirname(os.path.realpath(__file__))
    file = path + '/' + 'textFiles' + '/' + "colours.txt"
    
    colourDict = messageFeatures.convert_to_dict(file)

    if name == 'random':
        colour = random.choice(list(colourDict.values()))
    elif name not in colourDict:
        colour = (255,255,255,255)
    else:
        colour = colourDict[name]

    return colour


# def getcolort():
#     path = os.path.dirname(os.path.realpath(__file__))
#     file = path + '/' + 'textFiles' + '/' + "colours.txt"
#     with open(file,"r",encoding='utf-8') as f:
#         colours = f.read()
#     colourDict = ast.literal_eval(colours)

#     colour = random.choice(list(colourDict.values()))
#     print(colour)

# getcolort()
