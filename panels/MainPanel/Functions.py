import bpy
import os
from ...methods import manifest, APISearchService, RippingExportService

def ForceRefreshUI(self, context):
    return None

def SearchAPI(self, context):
    bpy.types.WindowManager.d2ci_search_results_manager.ClearCollectionAndFolder()
    apiSearch = context.window_manager.d2ci.D2APISearchBar
    APISearchService.GetAPISearchResultsByName(apiSearch, context)
    return {'FINISHED'}

def RipAndExportModel(self, context):
    RippingExportService.RipModelAndExport(context)
    return {'FINISHED'}

def SaveSettings(self, context):
    #Validate D2 Package Path
    selectedDestiny2PackagesFolder = context.window_manager.d2ci.D2PackageFilePath
    if not os.path.exists(selectedDestiny2PackagesFolder):
        self.report({"ERROR_INVALID_INPUT"}, "D2 Package Directory is not a real path. Please select another directory.")
        return {'CANCELLED'}
    
    selectedPackagePathIsValid = manifest.ValidateDestiny2PackageFolderLocation(selectedDestiny2PackagesFolder)
    if not selectedPackagePathIsValid:
        self.report({"ERROR_INVALID_INPUT"}, "D2 Package Directory selected is invalid, please select the correct directory.")
        return {'CANCELLED'}
    
    #Validate Output Dir
    selectedDestiny2OutputFolder = context.window_manager.d2ci.D2OutputFilePath
    if not os.path.exists(selectedDestiny2OutputFolder):
        self.report({"ERROR_INVALID_INPUT"}, "Output Directory is not a real path. Please select another directory.")
        return {'CANCELLED'}
    
    #Save
    context.window_manager.d2ci.D2SaveSettingsIsEnabled = False
    bpy.types.WindowManager.d2ci_config.SetConfigItem('General', 'Destiny2PackageFileLocation', selectedDestiny2PackagesFolder)
    bpy.types.WindowManager.d2ci_config.SetConfigItem('General', 'Destiny2OutputFileLocation', selectedDestiny2OutputFolder)

    selectedNumberOfRows = context.window_manager.d2ci.D2SearchResultsRows
    bpy.types.WindowManager.d2ci_config.SetConfigItem('General', 'APINumberOfSearchRows', str(selectedNumberOfRows))

    manifest.LoadD2Database(context)
    return {'FINISHED'}

def MainPanelMenu(context):
    option = context
    return option

def ForceSaveDueToConfigChange(self, context):
    context.window_manager.d2ci.HasModifiedConfig = True
    bpy.types.WindowManager.d2ci_config.HasModifiedConfig = True

def GetMainPanelTabs(self, context):
    return bpy.types.WindowManager.d2ci_config.GetMainPanelTabsAsEnum()

def GetSearchResultCollection(self, context):
    return bpy.types.WindowManager.d2ci_search_results_manager.GetCollectionAsEnum()

def SelectSearchResult(self, context):
    try:
        bpy.types.WindowManager.d2ci_search_results_manager.SelectEnumItem(int(context.window_manager.d2ci.SearchResultsEnum))
    except:
        bpy.types.WindowManager.d2ci_search_results_manager.ClearEnumItem()