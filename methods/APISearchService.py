
import os
from ..methods import helpermethods
from ..methods import database
from ..methods import webcalls
def GetAPISearchResultsByName(searchText):
    ImageCollection = {}
    queryResults = database.QueryManifestByName('DestinyInventoryItemDefinition', searchText)
    imageInfoObj = []
    for key, value in queryResults.items():
        imageInfo = [key, value.get('displayProperties').get('name'), value.get('displayProperties').get('icon')]
        imageInfoObj.append(imageInfo)
        ImageCollection[key] = [value.get('displayProperties').get('name'), os.path.join(helpermethods.GetProjectTempImagePath(), str(key)+ ".jpg")]
    webcalls.SaveImagesFromSearch(imageInfoObj)
    return ImageCollection