import os
import pathlib
from google_images_search import GoogleImagesSearch

try:
    GTOKEN = os.environ["GTOKEN"]
    GUSER = os.environ["GUSER"]
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    GTOKEN = os.environ.get("GOOGLETOKEN")
    GUSER = os.environ.get("GOOGLEUSER")


def ImgSearch(query):
    gis = GoogleImagesSearch(GTOKEN, GUSER)
    folder = (
        os.path.split(os.getcwd())[0]
        + "/"
        + os.path.split(os.getcwd())[1]
        + "/tempImages"
    )

    _search_params = {
        "q": query,
        "num": 1,
        "safe": "off",
        "fileType": "jpg",
        "imgType": "photo",
        "imgSize": "LARGE",
    }

    gis.search(search_params=_search_params, path_to_dir=folder)
    file = os.listdir(folder)

    file = folder + "/" + file[0]

    return file

