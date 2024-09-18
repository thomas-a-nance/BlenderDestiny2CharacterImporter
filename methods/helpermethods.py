import bpy
import os
import configparser
import asyncio
import tempfile
import json
from pathlib import Path

ProjectLocalStorageFolderName = "BlenderD2CI"
ItemDefinitionLocalStorageFolderName = "Destiny2ItemDefinition"
DownloadInProgressIndicatorFileName = "download_in_progress"

def getAsyncioLoop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        return asyncio.get_event_loop()

def GetProjectLocalPath():
    return os.path.join(Path(tempfile.gettempdir()).parent, ProjectLocalStorageFolderName)

def GetProjectTempImagePath():
    return os.path.join(GetProjectLocalPath(), "TempImages")

def GetProjectResourcesPath():
    return os.path.join(GetProjectLocalPath(), "Resources")

def GetManifestLocalPath():
    return os.path.join(GetProjectResourcesPath(), "Manifest.content")

#region Config
class ConfigManager():
    config = configparser.ConfigParser()
    configFileName = os.path.join(tempfile.gettempdir(), "BlenderD2CI", "config.ini")
    configOptions = '''{
            "General": {
                "ManifestVersionNumber": "",
                "Destiny2PackageFileLocation": ""
            }
        }'''

    def __destroy__(self):
        self.config = None

    def InitConfig(self):
        self.config.read(self.configFileName)
        configJsonDefaults = json.loads(self.configOptions)
        for category in configJsonDefaults:
            if category not in self.config:
                self.config[category] = {}
            for attribute, value in configJsonDefaults[category].items():
                if attribute not in self.config[category]:
                    self.config[category][attribute] = value

        self.UpdateConfigFile()

    def UpdateConfigFile(self):
        with open(self.configFileName, 'w') as configfile:
            self.config.write(configfile)

    def GetConfigItem(self, category, key):
        self.config.read(self.configFileName)
        if category not in self.config:
            return None
        categoryList = self.config[category]
        
        if not key in categoryList:
            return None
        return categoryList[key]

    def SetConfigItem(self, category, key, value):
        self.config.read(self.configFileName)
        if category not in self.config:
            return None
        categoryList = self.config[category]
        
        if not key in categoryList:
            return None
        categoryList[key] = value
        self.UpdateConfigFile()
        return True
#endregion

#region Icons
class CustomIconManager():
    IconCollection = {}
    IconDirectory = os.path.join(Path(os.path.dirname(__file__)).parent, "Resources", "images")
    PatchSignal = "PATCHME:"

    def __init__(self):
        self.IconCollection = bpy.utils.previews.new()

    def __destroy__(self):
        bpy.utils.previews.remove(self.IconCollection)

    def SetPatchSignal(self, name):
        return self.PatchSignal + name

    def GetIconId(self, identifier):
        if os.path.exists(os.path.join(self.IconDirectory, identifier + ".png")):
            return self.GetIcon(identifier).icon_id
        return "QUESTION"

    def GetIcon(self, identifier):
        if identifier in self.IconCollection:
            return self.IconCollection[identifier]
        
        return self.IconCollection.load(identifier, os.path.join(self.IconDirectory, identifier + ".png"), "IMAGE")        
#endregion