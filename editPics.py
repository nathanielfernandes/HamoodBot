import os
import pathlib

import random
# import cv2

from PIL import Image, ImageDraw, ImageFont

# import requests

path = os.path.dirname(os.path.realpath(__file__))

def addText(imageName, fontSize, textColor, firstText, secondText, thirdText, firstPos, secondPos, thirdPos, new):
    folder = path + '/' + "memePics"
    image = folder + '/' + imageName
    edited = folder + '/' + new

    fontPath = folder + '/' + 'arialbold.ttf'
    if ('/' in firstText) or ('/' in secondText) or ('/' in thirdText):
        fontSize -= 10
        
    firstText = firstText.replace('/', '\n')
    secondText = secondText.replace('/', '\n')
    thirdText = thirdText.replace('/', '\n')

    image = Image.open(image)   
    font_type = ImageFont.truetype(fontPath, fontSize)
    draw = ImageDraw.Draw(image)
    draw.text(xy=(firstPos[0], firstPos[1]), text=firstText, fill=(textColor), font=font_type)
    draw.text(xy=(secondPos[0], secondPos[1]), text=secondText, fill=(textColor), font=font_type)
    draw.text(xy=(thirdPos[0], thirdPos[1]), text=thirdText, fill=(textColor), font=font_type)
    #image.show()
    image.save(edited)
    return edited

# def scrape(imgURL, saveDir):
#     img_data = requests.get(imgURL).content
#     with open(saveDir, 'wb') as handler:
#         handler.write(img_data)

def randomNumber():
    char = '1234567890'
    combo = ''
    for i in range(12):
        num = random.choice(char)
        combo += num
        
    return combo

# def getClasifier(identity):
#     folder = path + '/' + 'classifiers'
    
#     types = ['eyes', 'faces', 'cats']
#     class_list = ["haarcascade_eye_tree_eyeglasses.xml", "haarcascade_frontalface_alt_tree.xml", "haarcascade_frontalcatface_extended.xml"]
    
#     loc = types.index(identity)
#     folder = folder + '/' + class_list[loc]

#     return folder


# def addFilter(img, filterImage, filterType, rotate):
#     folder = path + '/' + "memePics"
#     background = Image.open(img)
#     foreground = Image.open(folder + '/' + filterImage)

#     image = cv2.imread(img)

#     classifier = getClasifier(filterType)
#     eye_cascade = cv2.CascadeClassifier(classifier)

#     eyes = eye_cascade.detectMultiScale(image, scaleFactor = 1.1, minNeighbors = 5)

#     for (ex, ey, ew, eh) in eyes:
#         if rotate:
#             rt = random.randint(1, 3600)
#             foreground = foreground.rotate(rt, expand=False)
#         fore = foreground.resize((ew, eh), 0)
#         background.paste(fore, (ex, ey), fore)

#     identity = randomNumber()
#     identity = str(identity) + '.png'
    
#     finalName = folder + '/' + identity
#     background.save(finalName)

#     return finalName



# def googlyEyes(img):
#     folder = path + '/' + "memePics"
#     background = Image.open(img)
#     foreground = Image.open(folder + '/' + "googlyEye.png")

#     image = cv2.imread(img)

#     eye_cascade = cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")

#     eyes = eye_cascade.detectMultiScale(image, scaleFactor = 1.1, minNeighbors = 5)

#     for (ex, ey, ew, eh) in eyes:
#         rt = random.randint(1, 3600)
#         foreground = foreground.rotate(rt, expand=False)
#         fore = foreground.resize((ew,eh), 0)
#         background.paste(fore, (ex, ey), fore)
#         #cv2.rectangle(image, (ex, ey), (ex+ew, ey+eh), (0,0,255), 6)
    
#     identity = randomNumber()
#     identity = str(identity) + '.png'


#     finalName = folder + '/' + identity#"googlyfied.png"
#     background.save(finalName)

#     return finalName



# def clownFace(img):
#     folder = path + '/' + "memePics"
#     background = Image.open(img)
#     foreground = Image.open(folder + '/' + "clownFace.png")

#     image = cv2.imread(img)

#     face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")

#     faces = face_cascade.detectMultiScale(image, scaleFactor = 1.1, minNeighbors = 4)

#     for (ex, ey, ew, eh) in faces:
#         #rt = random.randint(1, 3600)
#         #foreground = foreground.rotate(rt, expand=False)
#         fore = foreground.resize((ew,eh), 0)
#         background.paste(fore, (ex, ey), fore)
#         #cv2.rectangle(image, (ex, ey), (ex+ew, ey+eh), (0,0,255), 6)

#     identity = randomNumber()
#     identity = str(identity) + '.png'

#     finalName = folder + '/' + identity #"clown_Faced.png"
#     background.save(finalName)

#     return finalName


# def catFace(img):
#     folder = path + '/' + "memePics"
#     background = Image.open(img)
#     foreground = Image.open(folder + '/' + "cryingCat.png")

#     image = cv2.imread(img)

#     face_cascade = cv2.CascadeClassifier("haarcascade_frontalcatface_extended.xml")

#     faces = face_cascade.detectMultiScale(image, scaleFactor = 1.1, minNeighbors = 4)

#     for (ex, ey, ew, eh) in faces:
#         #rt = random.randint(1, 3600)
#         #foreground = foreground.rotate(rt, expand=False)
#         fore = foreground.resize((ew,eh), 0)
#         background.paste(fore, (ex, ey), fore)
#         #cv2.rectangle(image, (ex, ey), (ex+ew, ey+eh), (0,0,255), 6)

#     identity = randomNumber()
#     identity = str(identity) + '.png'

#     finalName = folder + '/' + identity #"clown_Faced.png"
#     background.save(finalName)

#     return finalName


def deleteImage(file):
    os.remove(file)
#nameOne = 'nathan'
#addText('worthlessImage.jpg', 180, (0,0,0), nameOne, ' ', ' ', [300, 300], [0, 0], [0, 0], 'WORTHLESS.jpg')
#editImage('drakeImage.jpg', 80, (0,0,0), "nathan", "asdsadsad", "asdsads", [150, 525], [610, 250], [610, 850], 'DRAKE.jpg')

