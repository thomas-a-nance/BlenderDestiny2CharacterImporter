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
    IconCollection = None
    IconDirectory = os.path.join(Path(os.path.dirname(__file__)).parent, "Resources", "images")
    PatchSignal = "PATCHME:"

    def __destroy__(self):
        self.UnloadIcon()

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

    def LoadIcons(self):
        self.IconCollection = bpy.utils.previews.new()

    def UnloadIcon(self):
        bpy.utils.previews.remove(self.IconCollection)

    def PatchIcons(self, cls):
        """because properties are defined in __annotation__ space, we cannot get custom icon value as icons are not registered yet
        thus we need to re-sample the icons right before registering the PropertyGroup, this function will patch EnumProperty when needed"""

        def IsPatchNeeded(itm):
            """check if this item need to be patched, if the icon element of the item has a patchsignal"""
            return type(itm[3]) is str and itm[3].startswith(self.PatchSignal) #3rd element of an item is always the icon, see blender doc

        def PatchItem(itm):
            """patch icon element of an item if needed"""
            if IsPatchNeeded(itm):
                return tuple(self.GetIconId(e.replace(self.PatchSignal,"")) if (type(e) is str and e.startswith(self.PatchSignal)) else e for e in itm)
            return itm

        #for all EnumProperties initialized in cls.annotation space, 
        #that have more than 3 element per items 
        #& have at least one icon str value with the patch signal

        for propname,prop in [(propname,prop) for propname,prop in cls.__annotations__.items() 
                if (repr(prop.function)=="<built-in function EnumProperty>")
                and (len(prop.keywords["items"][0])>3)
                and len([itm for itm in prop.keywords["items"] if IsPatchNeeded(itm)])
                ]:

            #if found monkey-patch new items tuple w correct icon values
            prop.keywords["items"] = tuple(PatchItem(itm) for itm in prop.keywords["items"])

            #print(f"icon patched: {cls}{propname}")
            continue

        return cls 
#endregion