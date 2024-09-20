import bpy
import os
from ..methods import helpermethods
from ..methods import database
from ..methods import webcalls

@helpermethods.background
def GetAPISearchResultsByName(searchText, context):
    try:
        context.window_manager.d2ci.IsSearchingAPI = True
        context.window_manager.d2ci.SearchResultsText = "Searching Database..."
        queryResults = database.QueryManifestByName('DestinyInventoryItemDefinition', searchText)
        numOfFoundResults = str(len(queryResults.keys()))

        os.makedirs(helpermethods.GetProjectTempImagePath(), mode=0o777, exist_ok=True)
        imgCount = 0
        for key, value in queryResults.items():
            imgCount += 1
            context.window_manager.d2ci.SearchResultsText = f"Found {numOfFoundResults} result{'s' if numOfFoundResults == '1' else ''}. Downloading image {str(imgCount)}/{numOfFoundResults}..."
            GetAndSaveImage(value.get('displayProperties').get('icon'), os.path.join(helpermethods.GetProjectTempImagePath(), str(key)+ ".jpg"))

        bpy.types.WindowManager.d2ci_search_results_manager.SetQueryResultsFromSearch(queryResults)
        context.window_manager.d2ci.IsSearchingAPI = False

        
        context.window_manager.d2ci.SearchResultsText = f"Found {numOfFoundResults} result{'s' if numOfFoundResults == '1' else ''}"
    except Exception as e:
        context.window_manager.d2ci.IsSearchingAPI = False
        context.window_manager.d2ci.SearchResultsText = "Failed to query the database."

def GetAndSaveImage(url, downloadName):
    path = "https://bungie.net" + url
    imageData = webcalls.Get(path)
    if imageData.status_code == 200:
        with open(downloadName, 'wb') as f:
            for chunk in imageData:
                f.write(chunk)