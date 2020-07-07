import os
import formatMsg
import pathlib
from google_images_search import GoogleImagesSearch

from boto.s3.connection import S3Connection
s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])

def ImgSearch(query):
# define search params:
    #query = formatMsg.remove(query, '(', ')', "'", ",")
    gis = GoogleImagesSearch(GTOKEN, GUSER)
    path = os.path.dirname(os.path.realpath(__file__))
    folder = path + '/' + "tempImages"
    
    _search_params = {
        'q': query,
        'num': 1,
        'safe': 'off',
        'fileType': 'jpg',
        'imgType': 'photo',
        'imgSize': 'LARGE',
    }

    gis.search(search_params=_search_params, path_to_dir=folder)
    file = (os.listdir(folder))
    
    file = folder + '/' + file[0]

    return file

def deleteImage(file):
    os.remove(file)

