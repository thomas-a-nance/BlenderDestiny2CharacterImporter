import bpy
from ...methods import helpermethods

class VIEW3D_PG_D2CI_Props(bpy.types.PropertyGroup):
    D2PackageFilePath: bpy.props.StringProperty(
        name="D2 Packages Folder",
        description="Path to Destiny 2 packages folder",
        default=bpy.types.WindowManager.d2ci_config.GetConfigItem('General','Destiny2PackageFileLocation') or "",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    D2APISearchBar: bpy.props.StringProperty(
        name="API Search",
        description="Search the D2 API for an item",
        default="",
        maxlen=1024
    )

    MainPanelEnum: bpy.props.EnumProperty(
        name = 'Main Panel',
        description = 'D2CI Main Panel',
        items = [
            ('BAG', 'Build-A-Guardian', 'Build a guardian from Destiny 2 to import into the scene', bpy.types.WindowManager.d2ci_icons.GetIconId("bag"), 0),
            ('SETTINGS', 'Settings', 'Modify settings for D2CI', "SETTINGS", 1)
        ],
        default = 'BAG'
    )