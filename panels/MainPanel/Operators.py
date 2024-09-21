import bpy
from ..MainPanel import Functions

class UI_OT_D2CI_SearchAPI(bpy.types.Operator):
    bl_idname = "ui.d2ci_searchapi"
    bl_label = "Search API"
    bl_icon = "VIEWZOOM"
    bl_description = "Search the D2 API for an item"

    def execute(self, context):
        return Functions.SearchAPI(self, context)
    
class UI_OT_D2CI_ClearCache(bpy.types.Operator):
    bl_idname = "ui.d2ci_clearcache"
    bl_label = "Clear Cache"
    bl_icon = "BRUSH_DATA"
    bl_description = "Clears the cache of images from query searches"
    
    def execute(self, context):
        bpy.types.WindowManager.d2ci_search_results_manager.ClearCache()
        return {'FINISHED'}

class UI_OT_D2CI_Reinitialize(bpy.types.Operator):
    bl_idname = "ui.d2ci_reinitialize"
    bl_label = "Reinitialize"
    bl_icon = "TRASH"
    bl_description = "Clears the version number, forcing the manifest to be redownloaded on save"
    
    def execute(self, context):
        bpy.types.WindowManager.d2ci_config.SetConfigItem('General','ManifestVersionNumber','')
        return {'FINISHED'}
    
class UI_OT_D2CI_SaveSettings(bpy.types.Operator):
    bl_idname = "ui.d2ci_save_settings"
    bl_label = "Save Settings"
    bl_description = "Downloads the manifest to query data"

    def execute(self, context):
        return Functions.SaveSettings(self, context)
