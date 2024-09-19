import bpy
import os
from ..methods import helpermethods
from ..methods import database
from ..methods import webcalls
def GetAPISearchResultsByName(searchText):
    queryResults = database.QueryManifestByName('DestinyInventoryItemDefinition', searchText)
    imageInfoObj = []
    for key, value in queryResults.items():
        imageInfo = [value.get('displayProperties').get('icon'), os.path.join(helpermethods.GetProjectTempImagePath(), str(key)+ ".jpg")]
        imageInfoObj.append(imageInfo)
    webcalls.SaveImagesFromSearch(imageInfoObj)
    return queryResults