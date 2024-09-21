import bpy
import os
import asyncio
import tempfile
from pathlib import Path

ProjectLocalStorageFolderName = "BlenderD2CI"
ItemDefinitionLocalStorageFolderName = "Destiny2ItemDefinition"
DownloadInProgressIndicatorFileName = "download_in_progress"
    
def getAsyncioLoop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        asyncio.new_event_loop()
        return asyncio.get_event_loop()

def background(f):
    def wrapped(*args, **kwargs):
        return getAsyncioLoop().run_in_executor(None, f, *args, **kwargs)

    return wrapped

def GetProjectLocalPath():
    return os.path.join(Path(tempfile.gettempdir()).parent, ProjectLocalStorageFolderName)

def GetProjectSearchResultsImagePath():
    return os.path.join(GetProjectLocalPath(), "SearchResults")

def GetProjectTempImagePath():
    return os.path.join(GetProjectLocalPath(), "TempImages")

def GetProjectCacheImagePath():
    return os.path.join(GetProjectLocalPath(), "Cache")

def GetProjectResourcesPath():
    return os.path.join(GetProjectLocalPath(), "Resources")

def GetManifestLocalPath():
    return os.path.join(GetProjectResourcesPath(), "Manifest.content")

def GetProjectPath():
    return Path(os.path.dirname(__file__)).parent

def GetProjectImagePath():
    return os.path.join(GetProjectPath(), "Resources", "images")

def GetProjectMDEPath():
    return os.path.join(GetProjectPath(), "Resources", "MDE")