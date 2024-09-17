import bpy
import os
import configparser
import asyncio
import tempfile
import json
from pathlib import Path
import shutil

config = configparser.ConfigParser()
configFileName = os.path.join(tempfile.gettempdir(), "BlenderD2CI", "config.ini")
configOptions = '''{
        "General": {
            "ManifestVersionNumber": "",
            "Destiny2PackageFileLocation": ""
        }
    }'''

ProjectLocalStorageFolderName = "BlenderD2CI"
ItemDefinitionLocalStorageFolderName = "Destiny2ItemDefinition"
DownloadInProgressIndicatorFileName = "download_in_progress"

IconCollection = None
IconDirectory = os.path.join(Path(os.path.dirname(__file__)).parent, "Resources", "images")

def __destroy__():
    config = None
    UnloadIcon()

def getAsyncioLoop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        return asyncio.get_event_loop()

def GetProjectLocalPath():
    return os.path.join(tempfile.gettempdir(), ProjectLocalStorageFolderName)

def GetProjectResourcesPath():
    return os.path.join(GetProjectLocalPath(), "Resources")

def GetManifestLocalPath():
    return os.path.join(GetProjectResourcesPath(), "Manifest.content")

#region Config
def InitConfig():
    config.read(configFileName)
    configJsonDefaults = json.loads(configOptions)
    for category in configJsonDefaults:
        if category not in config:
            config[category] = {}
        for attribute, value in configJsonDefaults[category].items():
            if attribute not in config[category]:
                config[category][attribute] = value

    UpdateConfigFile()

def UpdateConfigFile():
    with open(configFileName, 'w') as configfile:
        config.write(configfile)

def GetConfigItem(category, key):
    config.read(configFileName)
    if category not in config:
        return None
    categoryList = config[category]
    
    if not key in categoryList:
        return None
    return categoryList[key]

def SetConfigItem(category, key, value):
    config.read(configFileName)
    if category not in config:
        return None
    categoryList = config[category]
    
    if not key in categoryList:
        return None
    categoryList[key] = value
    UpdateConfigFile()
    return True
#endregion

#region Iconszzz
def GetIconId(identifier):
    if os.path.exists(os.path.join(IconDirectory, identifier + ".png")):
        return GetIcon(identifier).icon_id
    return "QUESTION"

def GetIcon(identifier):
    if identifier in IconCollection:
        return IconCollection[identifier]
    
    return IconCollection.load(identifier, os.path.join(IconDirectory, identifier + ".png"), "IMAGE")

def LoadIcons():
    global IconCollection
    IconCollection = bpy.utils.previews.new()

def UnloadIcon():
    bpy.utils.previews.remove(IconCollection)

class IconsMock:
    def get(self, identifier):
        return GetIcon(identifier)

icons = IconsMock()
#endregion