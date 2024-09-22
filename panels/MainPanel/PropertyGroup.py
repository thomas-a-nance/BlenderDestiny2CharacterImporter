import bpy
from ..MainPanel import Functions

class UI_PG_D2CI_Props(bpy.types.PropertyGroup):
    D2PackageFilePath: bpy.props.StringProperty(
        name="D2 Packages Directory",
        description="Directory to Destiny 2 packages folder",
        default=bpy.types.WindowManager.d2ci_config.GetConfigItem('General','Destiny2PackageFileLocation') or "",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    D2OutputFilePath: bpy.props.StringProperty(
        name="D2 Output Directory",
        description="Directory to where to download models/data",
        default=bpy.types.WindowManager.d2ci_config.GetConfigItem('General','Destiny2OutputFileLocation') or "",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    D2SaveSettingsIsEnabled: bpy.props.BoolProperty(
        name = 'D2SaveSettingsIsEnabled',
        description = 'Should the Save Settings button be enabled?',
        default = True,
        update=Functions.ForceRefreshUI
    )

    D2APISearchBar: bpy.props.StringProperty(
        name="API Search",
        description="Search the D2 API for an item",
        default="",
    )

    D2SearchResultsRows: bpy.props.IntProperty(
        name="Rows Per Search",
        description="Number of rows returned for a search result (8 per row).",
        default=int(bpy.types.WindowManager.d2ci_config.GetConfigItem('General','APINumberOfSearchRows')),
        min=1
    )

    MainPanelEnum: bpy.props.EnumProperty(
        name = 'Main Panel',
        description = 'D2CI Main Panel',
        items = Functions.GetMainPanelTabs,
        default = (0 if bpy.types.WindowManager.d2ci_config.ShouldShowAllMainPanelTabs() else len(bpy.types.WindowManager.d2ci_config.GetMainPanelTabsAsEnum()))
    )

    SearchResultsText: bpy.props.StringProperty(
        name = 'SearchResultsText',
        description = 'D2CI Search Results Count',
        default = "",
        update=Functions.ForceRefreshUI
    )

    IsSearchingAPI: bpy.props.BoolProperty(
        name = 'IsSearchingAPI',
        description = 'Is performing D2CI Search Results',
        default = False,
        update=Functions.ForceRefreshUI
    )

    SearchResultsEnum: bpy.props.EnumProperty(
        name = 'SearchResults',
        description = 'D2CI Search Results Enum',
        items = Functions.GetSearchResultCollection,
        update=Functions.SelectSearchResult
    )

    RippingExportText: bpy.props.StringProperty(
        name = 'RippingExportText',
        description = 'Ripping/Export status',
        default = "",
        update=Functions.ForceRefreshUI
    )

    IsRippingExport: bpy.props.BoolProperty(
        name = 'IsRippingExport',
        description = 'Is performing D2CI Ripping/Export',
        default = False,
        update=Functions.ForceRefreshUI
    )