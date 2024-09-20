import bpy
import os
from ..methods import helpermethods
from ..methods import database
from ..methods import webcalls

@helpermethods.background
def GetAPISearchResultsByName(searchText, context):
    context.window_manager.d2ci.ShowSearchResultsCount = False
    context.window_manager.d2ci.IsSearchingAPI = True
    context.window_manager.d2ci.SearchResultsCount = 0
    queryResults = database.QueryManifestByName('DestinyInventoryItemDefinition', searchText)
    imageInfoObj = []
    for key, value in queryResults.items():
        imageInfo = [value.get('displayProperties').get('icon'), os.path.join(helpermethods.GetProjectTempImagePath(), str(key)+ ".jpg")]
        imageInfoObj.append(imageInfo)
        
    webcalls.SaveImagesFromSearch(imageInfoObj)
    bpy.types.WindowManager.d2ci_search_results_manager.SetQueryResultsFromSearch(queryResults)
    context.window_manager.d2ci.IsSearchingAPI = False
    context.window_manager.d2ci.ShowSearchResultsCount = True
    context.window_manager.d2ci.SearchResultsCount = len(queryResults.keys())