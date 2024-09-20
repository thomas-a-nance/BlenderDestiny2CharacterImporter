import bpy
from ...methods import manifest, helpermethods, APISearchService

def ForceRefreshUI(self, context):
    return None

def SearchAPI(self, context):
    bpy.types.WindowManager.d2ci_search_results_manager.ClearCollectionAndFolder()
    apiSearch = context.window_manager.d2ci.D2APISearchBar
    APISearchService.GetAPISearchResultsByName(apiSearch, context)
    return {'FINISHED'}

def SaveSettings(self, context):
    selectedDestiny2PackagesFolder = context.window_manager.d2ci.D2PackageFilePath
    selectedPackagePathIsValid = manifest.ValidateDestiny2PackageFolderLocation(selectedDestiny2PackagesFolder)
    if not selectedPackagePathIsValid:
        self.report({"ERROR_INVALID_INPUT"}, "Directory selected is invalid, please select the correct packages directory.")
        return {'CANCELLED'}
    bpy.types.WindowManager.d2ci_config.SetConfigItem('General', 'Destiny2PackageFileLocation', selectedDestiny2PackagesFolder)
    bpy.types.WindowManager.d2ci_config.IsPopulatingManifestConfig = True
    manifest.LoadD2Database()
    return {'FINISHED'}

def MainPanelMenu(context):
    option = context
    return option

def GetSearchResultCollection(self, context):
    return bpy.types.WindowManager.d2ci_search_results_manager.GetCollectionAsEnum()

def SelectSearchResult(self, context):
    try:
        bpy.types.WindowManager.d2ci_search_results_manager.SelectEnumItem(int(context.window_manager.d2ci.SearchResultsEnum))
    except:
        bpy.types.WindowManager.d2ci_search_results_manager.ClearEnumItem()