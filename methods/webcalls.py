import asyncio
import requests
import os
from ..methods import helpermethods

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped

def Get(url, headers={}):
    return requests.get(url, headers=headers, timeout=None, stream=True)

def SaveImagesFromSearch(imageInfoObj):
    os.makedirs(helpermethods.GetProjectTempImagePath(), mode=0o777, exist_ok=True)

    for imageToGet in imageInfoObj:
        GetAndSaveImage(imageToGet[0], imageToGet[1])

    return

@background
def GetAndSaveImage(url, downloadName):
    path = "https://bungie.net" + url
    imageData = Get(path)
    if imageData.status_code == 200:
        with open(downloadName, 'wb') as f:
            for chunk in imageData:
                f.write(chunk)