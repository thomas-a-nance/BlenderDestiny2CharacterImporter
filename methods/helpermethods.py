import bpy
import os
import configparser
import asyncio
import tempfile
import json
import shutil
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

def GetProjectPath():
    return Path(os.path.dirname(__file__)).parent

def GetProjectImagePath():
    return os.path.join(GetProjectPath(), "Resources", "images")

#region Config
class ConfigManager():
    config = configparser.ConfigParser()
    configFileName = os.path.join(GetProjectLocalPath(), "config.ini")
    configOptions = '''{
            "General": {
                "ManifestVersionNumber": "",
                "Destiny2PackageFileLocation": ""
            }
        }'''

    def __del__(self):
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
    IconDirectory = GetProjectImagePath()

    def __init__(self):
        self.IconCollection = bpy.utils.previews.new()

    def __del__(self):
        bpy.utils.previews.remove(self.IconCollection)

    def GetIconId(self, identifier):
        if os.path.exists(os.path.join(self.IconDirectory, identifier + ".png")):
            return self.GetIcon(identifier).icon_id
        return "QUESTION"

    def GetIcon(self, identifier):
        if identifier in self.IconCollection:
            return self.IconCollection[identifier]
        
        return self.IconCollection.load(identifier, os.path.join(self.IconDirectory, identifier + ".png"), "IMAGE")

class SearchResultsManager():
    ResultsCollection = {}
    QueryResults = {}
    SearchResultsDirectory = GetProjectTempImagePath()
    ProjectImageDirectory = GetProjectImagePath()
    DefaultEngramImage = 'engram.png'
    IsNewCollection = True

    def __init__(self):
        self.ResultsCollection = bpy.utils.previews.new()

    def __del__(self):
        bpy.utils.previews.remove(self.ResultsCollection)

    def SetQueryResultsFromSearch(self, results):
        self.QueryResults = results

    def ClearCollectionAndFolder(self):
        self.ResetCollection()
        shutil.rmtree(self.SearchResultsDirectory, ignore_errors=True)
        os.makedirs(self.SearchResultsDirectory, mode=0o777, exist_ok=True)

    def ResetCollection(self):
        self.ResultsCollection.clear()
        self.IsNewCollection = True

    def GetCollectionAsEnum(self):
        enumItems = []

        if os.path.exists(self.SearchResultsDirectory) and len(os.listdir(self.SearchResultsDirectory)) > 0:
            for i, name in enumerate(os.listdir(self.SearchResultsDirectory)):
                filepath = os.path.join(self.SearchResultsDirectory, name)
                enumItems.append(self.GetItemForEnum(i+1, name, filepath))

        self.IsNewCollection = False
        return enumItems
    
    def GetItemForEnum(self, i, name, filepath):
        icon = self.ResultsCollection.get(name)
        if not icon:
            thumb = self.ResultsCollection.load(name, filepath, 'IMAGE')
        else:
            thumb = self.ResultsCollection[name]

        intFlag = True
        try:
            displayName = name
            itemId = int(Path(name).stem)
            if itemId in self.QueryResults.keys():
                displayName = self.QueryResults.get(itemId).get('displayProperties').get('name')

            return (name, displayName, "", thumb.icon_id, i)
        except:
            return (name, name, "", thumb.icon_id, i)
#endregion