import os
import pathlib

def getMedia(mix):
  
    mix -= 1
    path = os.path.dirname(os.path.realpath(__file__))
    folder = path + '/' + "media"

    content = os.listdir(folder)
    content = folder + '/' + content[mix]

    return content