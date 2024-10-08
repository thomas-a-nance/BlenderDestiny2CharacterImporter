import bpy
from .classes.SearchResultsManager import SearchResultsManager
from .classes.ConfigManager import ConfigManager
from .classes.CustomIconManager import CustomIconManager

bl_info = {
    "name" : "Destiny 2 Character Importer",
    "author" : "Thomas Nance",
    "description" : "",
    "blender" : (4, 2, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

bpy.types.WindowManager.d2ci_icons = CustomIconManager()
bpy.types.WindowManager.d2ci_search_results_manager = SearchResultsManager()
bpy.types.WindowManager.d2ci_config = ConfigManager()

from . import auto_load
auto_load.init()

from .panels.MainPanel import Panel, Operators, PropertyGroup

main_classes = (
    Panel.UI_PT_D2CI,
    Operators.UI_OT_D2CI_SaveSettings,
    Operators.UI_OT_D2CI_Reinitialize,
    Operators.UI_OT_D2CI_SearchAPI,
    Operators.UI_OT_D2CI_ClearCache,
    Operators.UI_OT_D2CI_RunRipperExport,
    PropertyGroup.UI_PG_D2CI_Props,
)

def register():
    bpy.types.WindowManager.d2ci_config.InitConfig()

    for cls in main_classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.d2ci = bpy.props.PointerProperty(type=PropertyGroup.UI_PG_D2CI_Props)
    bpy.types.WindowManager.d2ci_search_results_manager.ClearCollectionAndFolder()

def unregister():
    for cls in reversed(main_classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.d2ci
    bpy.types.WindowManager.d2ci_search_results_manager.ClearCollectionAndFolder()
