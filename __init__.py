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

#packages
from . import auto_load
auto_load.init()

from .panels import MainPanel
main_classes = (
    MainPanel.VIEW3D_PT_D2CI,
    MainPanel.VIEW3D_OT_D2CI_SaveSettings,
    MainPanel.VIEW3D_OT_D2CI_Reinitialize,
)

def register():
    helpermethods.LoadIcons()
    helpermethods.InitConfig()

    from bpy.utils import register_class
    bpy.utils.register_class(helpermethods.patch_custom_icons(MainPanel.VIEW3D_PG_D2CI_Props))
    for cls in main_classes:
        register_class(cls)

    bpy.types.WindowManager.d2ci = bpy.props.PointerProperty(type=MainPanel.VIEW3D_PG_D2CI_Props)

def unregister():
    from bpy.utils import unregister_class
    helpermethods.UnloadIcon()
    for cls in reversed(main_classes):
        unregister_class(cls)
    del bpy.types.WindowManager.d2ci