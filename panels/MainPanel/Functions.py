import bpy
from ...methods import manifest
from ...methods import APISearchService
from ...panels.MainPanel import Functions

def CheckForSearchAPI(self, context):
    bpy.ops.ui.d2ci_checkforsearchapi('INVOKE_DEFAULT')
    return

def SearchAPI(self, context):
    bpy.types.WindowManager.d2ci_search_results_manager.ClearCollectionAndFolder()
    apiSearch = context.window_manager.d2ci.D2APISearchBar
    queryResults = APISearchService.GetAPISearchResultsByName(apiSearch)
    bpy.types.WindowManager.d2ci_search_results_manager.SetQueryResultsFromSearch(queryResults)
    bpy.types.WindowManager.d2ci_search_results_manager.ResetCollection()
    return {'FINISHED'}

def SaveSettings(self, context):
    selectedDestiny2PackagesFolder = context.window_manager.d2ci.D2PackageFilePath
    selectedPackagePathIsValid = manifest.ValidateDestiny2PackageFolderLocation(selectedDestiny2PackagesFolder)
    if not selectedPackagePathIsValid:
        self.report({"ERROR_INVALID_INPUT"}, "Directory selected is invalid, please select the correct packages directory.")
        return {'CANCELLED'}
    bpy.types.WindowManager.d2ci_config.SetConfigItem('General', 'Destiny2PackageFileLocation', selectedDestiny2PackagesFolder)
    manifest.LoadD2Database()
    return {'FINISHED'}

def MainPanelMenu(context):
    option = context
    return option

def GetSearchResultCollection(self, context):
    return bpy.types.WindowManager.d2ci_search_results_manager.GetCollectionAsEnum()