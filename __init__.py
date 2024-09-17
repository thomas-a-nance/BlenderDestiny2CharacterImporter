import bpy
import asyncio
import bpy.utils.previews  # type: ignore
from .panels import MainPanel

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

main_classes = (
    MainPanel.VIEW3D_PT_Destiny2_Character_Importer_Properties,
    MainPanel.VIEW3D_OT_Destiny2_Character_Importer_InitializeDatabase,
    MainPanel.VIEW3D_PT_Destiny2_Character_Importer,
    MainPanel.VIEW3D_OT_Destiny2_Character_Importer_DatabaseRefresh
)

def register():
    from .methods import helpermethods

    from bpy.utils import register_class
    for cls in main_classes:
        register_class(cls)

    helpermethods.InitConfig()
    bpy.types.Scene.d2ci = bpy.props.PointerProperty(type=MainPanel.VIEW3D_PT_Destiny2_Character_Importer_Properties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(main_classes):
        unregister_class(cls)
    del bpy.types.Scene.d2ci