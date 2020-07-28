import os
import pathlib
from google_images_search import GoogleImagesSearch

GTOKEN = os.environ['GTOKEN']
GUSER = os.environ['GUSER']

def ImgSearch(query):
    # define search params:
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

