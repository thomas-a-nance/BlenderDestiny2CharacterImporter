import bpy
import asyncio
import bpy.utils.previews  # type: ignore
from .methods import helpermethods

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

asyncio.set_event_loop(asyncio.new_event_loop())

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

bpy.types.WindowManager.d2ci_icons = helpermethods.CustomIconManager()
bpy.types.WindowManager.d2ci_config = helpermethods.ConfigManager()

from . import auto_load
auto_load.init()

from .panels.MainPanel import Panel, Operators, PanelGroups

main_classes = (
    Panel.VIEW3D_PT_D2CI,
    Operators.VIEW3D_OT_D2CI_SaveSettings,
    Operators.VIEW3D_OT_D2CI_Reinitialize,
    Operators.VIEW3D_OT_D2CI_SearchAPI,
    PanelGroups.VIEW3D_PG_D2CI_Props
)

def register():    
    bpy.types.WindowManager.d2ci_icons.LoadIcons()
    bpy.types.WindowManager.d2ci_icons.PatchIcons(PanelGroups.VIEW3D_PG_D2CI_Props)
    bpy.types.WindowManager.d2ci_config.InitConfig()

    for cls in main_classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.d2ci = bpy.props.PointerProperty(type=PanelGroups.VIEW3D_PG_D2CI_Props)

def unregister():
    bpy.types.WindowManager.d2ci_icons.UnloadIcon()
    for cls in reversed(main_classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.d2ci