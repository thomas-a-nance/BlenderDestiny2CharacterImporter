import bpy
from ...methods import helpermethods
from ...methods import manifest
from ...methods import APISearchService

class VIEW3D_OT_D2CI_SearchAPI(bpy.types.Operator):
    bl_idname = "view3d.d2ci_searchapi"
    bl_label = "Search API"
    bl_icon = "VIEWZOOM"
    bl_description = "Search the D2 API for an item"

    def execute(self, context):
        return SearchAPI(self, context)

class VIEW3D_OT_D2CI_Reinitialize(bpy.types.Operator):
    bl_idname = "view3d.d2ci_reinitialize"
    bl_label = "Reinitialize"
    bl_icon = "TRASH"
    bl_description = "Clears the version number, forcing the manifest to be redownloaded on save"
    
    def execute(self, context):
        bpy.types.WindowManager.d2ci_config.SetConfigItem('General','ManifestVersionNumber','')
        return {'FINISHED'}
    
class VIEW3D_OT_D2CI_SaveSettings(bpy.types.Operator):
    bl_idname = "view3d.d2ci_save_settings"
    bl_label = "Save Settings"
    bl_description = "Downloads the manifest to query data"

    def execute(self, context):
        return SaveSettings(self, context)



#region Functions & Enums
def SearchAPI(self, context):
    global ImageCollection
    ImageCollection = {}
    apiSearch = context.window_manager.d2ci.D2APISearchBar
    ImageCollection = APISearchService.GetAPISearchResultsByName(apiSearch)
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
#endregion