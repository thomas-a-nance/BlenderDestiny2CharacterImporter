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

PatchSignal = "PATCHME:"

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

def patch_custom_icons(cls):
    """because properties are defined in __annotation__ space, we cannot get custom icon value as icons are not registered yet
    thus we need to re-sample the icons right before registering the PropertyGroup, this function will patch EnumProperty when needed"""

    def patch_needed(itm):
        """check if this item need to be patched, if the icon element of the item has a patchsignal"""
        return type(itm[3]) is str and itm[3].startswith(PatchSignal) #3rd element of an item is always the icon, see blender doc

    def patch_item(itm):
        """patch icon element of an item if needed"""
        if patch_needed(itm):
            return tuple(GetIconId(e.replace(PatchSignal,"")) if (type(e) is str and e.startswith(PatchSignal)) else e for e in itm)
        return itm

    #for all EnumProperties initialized in cls.annotation space, 
    #that have more than 3 element per items 
    #& have at least one icon str value with the patch signal

    for propname,prop in [(propname,prop) for propname,prop in cls.__annotations__.items() 
               if (repr(prop.function)=="<built-in function EnumProperty>")
               and (len(prop.keywords["items"][0])>3)
               and len([itm for itm in prop.keywords["items"] if patch_needed(itm)])
               ]:

        #if found monkey-patch new items tuple w correct icon values
        prop.keywords["items"] = tuple(patch_item(itm) for itm in prop.keywords["items"])

        #print(f"icon patched: {cls}{propname}")
        continue

    return cls 
#endregion