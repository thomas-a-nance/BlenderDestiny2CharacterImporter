import requests
import os
from ..methods.helpermethods import GetProjectTempImagePath, background

def Get(url, headers={}):
    return requests.get(url, headers=headers, timeout=None, stream=True)