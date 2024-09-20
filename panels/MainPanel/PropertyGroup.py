import bpy
from ..MainPanel import Functions
from ...methods import helpermethods

class UI_PG_D2CI_Props(bpy.types.PropertyGroup):
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
    )

    MainPanelEnum: bpy.props.EnumProperty(
        name = 'Main Panel',
        description = 'D2CI Main Panel',
        items = [
            ('BAG', 'Build-A-Guardian', 'Build a guardian from Destiny 2 to import into the scene', bpy.types.WindowManager.d2ci_icons.GetIconId("bag"), 0),
            ('SETTINGS', 'Settings', 'Modify settings for D2CI', bpy.types.WindowManager.d2ci_icons.GetIconId("settings"), 1)
        ],
        default = 'BAG'
    )

    SearchResultsCount: bpy.props.IntProperty(
        name = 'SearchResultsCount',
        description = 'D2CI Search Results Count',
        default = 0,
        update=Functions.ForceRefreshUI
    )

    ShowSearchResultsCount: bpy.props.BoolProperty(
        name = 'ShowSearchResultsCount',
        description = 'Show D2CI Search Results Count',
        default = False
    )

    IsSearchingAPI: bpy.props.BoolProperty(
        name = 'IsSearchingAPI',
        description = 'Is performing D2CI Search Results',
        default = False
    )

    SearchResultsEnum: bpy.props.EnumProperty(
        name = 'SearchResults',
        description = 'D2CI Search Results Enum',
        items = Functions.GetSearchResultCollection,
        update=Functions.SelectSearchResult
    )