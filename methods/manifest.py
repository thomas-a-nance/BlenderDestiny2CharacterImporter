import bpy
import os
import requests
import zipfile
import shutil
from ..methods import webcalls
from ..methods import helpermethods

baseUrl = 'https://bungie.net'
manifestUrl = '/Platform/Destiny2/Manifest/'

def ValidateDestiny2PackageFolderLocation(folderPath):
    if not os.path.exists(folderPath):
        return False
    if(folderPath != bpy.types.WindowManager.d2ci_config.GetConfigItem('General','Destiny2PackageFileLocation')):
        return any(fname.endswith('.pkg') for fname in os.listdir(folderPath))
    return True

def LoadD2Database():
    loop = helpermethods.getAsyncioLoop()
    d2ManifestQuery = loop.run_until_complete(GetDestiny2ManifestFromAPI())
    d2Manifest = d2ManifestQuery.json()
    d2ManifestVersion = d2Manifest["Response"]["version"]
    d2ItemDefinitionURL = baseUrl + d2Manifest["Response"]["mobileWorldContentPaths"]["en"]
    folderPath = helpermethods.GetProjectResourcesPath()
    manifestPickle = helpermethods.GetManifestLocalPath()
    if os.path.exists(os.path.join(folderPath, helpermethods.DownloadInProgressIndicatorFileName)) or not os.path.exists(manifestPickle) or bpy.types.WindowManager.d2ci_config.GetConfigItem('General','ManifestVersionNumber') != d2ManifestVersion:
        loop.run_until_complete(DownloadManifestContent(d2ItemDefinitionURL, folderPath))

    elif bpy.types.WindowManager.d2ci_config.GetConfigItem('General','ManifestVersionNumber') == d2ManifestVersion:
        if not os.path.exists(manifestPickle):
            loop.run_until_complete(DownloadManifestContent(d2ItemDefinitionURL, folderPath))
 
    bpy.types.WindowManager.d2ci_config.SetConfigItem('General', 'ManifestVersionNumber', d2ManifestVersion)
    return 

async def GetDestiny2ManifestFromAPI():
    apiUrl = baseUrl + manifestUrl
    headers = {"Content-Type":"application/json", "X-API-KEY":"aa5aaca04c2d433f923e3cca8119dddf"}
    returnData = webcalls.Get(apiUrl, headers)
    return returnData

async def DownloadManifestContent(d2ItemDefinitionURL, folderPath):
    downloadIndicator = os.path.join(folderPath, helpermethods.DownloadInProgressIndicatorFileName)
    shutil.rmtree(folderPath, ignore_errors=True)
    os.makedirs(folderPath, mode=0o777, exist_ok=True)
    open(downloadIndicator, 'a').close()

    tmpFileLocation = os.path.join(folderPath, "MANZIP")
    manifestLocation = helpermethods.GetManifestLocalPath()
    headers = {"X-API-KEY":"aa5aaca04c2d433f923e3cca8119dddf"}
    r = requests.get(d2ItemDefinitionURL, headers=headers, timeout=None)
    with open(tmpFileLocation, "wb") as zip:
        zip.write(r.content)

    with zipfile.ZipFile(tmpFileLocation) as zip:
        name = zip.namelist()
        zip.extractall(folderPath)
    os.rename(os.path.join(folderPath, name[0]), manifestLocation)

    print("Database Built")
    os.remove(tmpFileLocation)
    os.remove(downloadIndicator)
    return