import os
import configparser
import asyncio
import tempfile
import json

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