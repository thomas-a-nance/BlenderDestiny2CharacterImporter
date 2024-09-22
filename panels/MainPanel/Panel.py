import bpy
import os
from .Operators import *
from ..MainPanel import Functions
    
# ------------------------------------------------------------------------
#    Panel UI
# ------------------------------------------------------------------------
class UI_PT_D2CI(bpy.types.Panel):  # class naming convention ‘CATEGORY_PT_name’
    #Blender Init
    bl_space_type = "VIEW_3D"  # 3D Viewport area (find list of values here https://docs.blender.org/api/current/bpy_types_enum_items/space_type_items.html#rna-enum-space-type-items)
    bl_region_type = "UI"  # Sidebar region (find list of values here https://docs.blender.org/api/current/bpy_types_enum_items/region_type_items.html#rna-enum-region-type-items)
    bl_category = "D2CI" # Sidebar name
    bl_label = "D2CI" # Panel Title

    def draw(self, context):
        ctx = context.window_manager.d2ci
        col = self.layout.column(align=True)
        row = col.row(align=True)
        row.alignment = 'RIGHT'
        row.scale_x = 2
        row.scale_y = 1.25
        
        if self.ShouldShowMainPanels(ctx) :
            row.prop(Functions.MainPanelMenu(ctx), 'MainPanelEnum', expand=True, icon_only=True)
        else:
            ctx.MainPanelEnum = "SETTINGS"
        
        match ctx.MainPanelEnum:
            case "BAG":
                self.DrawAPISearch(context)
            case _:
                self.DrawSettings(context)
    
    def ShouldShowMainPanels(self, context):
        return len(bpy.types.WindowManager.d2ci_config.GetConfigItem('General','ManifestVersionNumber')) != 0 \
                    and bpy.types.WindowManager.d2ci_config.GetConfigItem('General','Destiny2PackageFileLocation') == context.D2PackageFilePath \
                    and os.path.exists(bpy.types.WindowManager.d2ci_config.GetConfigItem('General','Destiny2PackageFileLocation')) \
                    and len(bpy.types.WindowManager.d2ci_config.GetConfigItem('General','Destiny2PackageFileLocation')) > 0 \
                    and bpy.types.WindowManager.d2ci_config.GetConfigItem('General','Destiny2OutputFileLocation') == context.D2OutputFilePath \
                    and os.path.exists(bpy.types.WindowManager.d2ci_config.GetConfigItem('General','Destiny2OutputFileLocation')) \
                    and len(bpy.types.WindowManager.d2ci_config.GetConfigItem('General','Destiny2OutputFileLocation')) > 0 \
                    and int(bpy.types.WindowManager.d2ci_config.GetConfigItem('General','APINumberOfSearchRows')) == context.D2SearchResultsRows

    def DrawAPISearch(self, context):
        ctx = context.window_manager.d2ci
        row = self.layout.row(align=True)
        row.alignment = "CENTER"
        row.label(text="Transmog Search")
        row = self.layout.row(align=True)
        row.prop(ctx, "D2APISearchBar", text="")

        searchButton = row.column()
        searchButton.operator(UI_OT_D2CI_SearchAPI.bl_idname, text="", icon=UI_OT_D2CI_SearchAPI.bl_icon)
        searchButton.enabled = not ctx.IsSearchingAPI
        if len(ctx.SearchResultsText) > 0:
            row = self.layout.row()
            row.alignment = "RIGHT"
            row.label(text=ctx.SearchResultsText)

        self.layout.separator(factor=2, type="LINE")

        if ctx.IsSearchingAPI:
            ctx.SearchResultsEnum = 'None'
            ctx.RippingExportText = ''
        
        nPanelWidth = context.region.width #280 Default
        searchResultWidth = 150
        nPanelViewSplit = 350

        if nPanelWidth < nPanelViewSplit:
            row = self.layout.split(factor = (searchResultWidth / nPanelWidth))
        else:
            row = self.layout.split(factor = (searchResultWidth / nPanelWidth))
            
        col = row.column()
        col.template_icon_view(ctx, 
            "SearchResultsEnum",
            show_labels=True,
            scale=6,
            scale_popup=5
        )
        
        selectedEntry = bpy.types.WindowManager.d2ci_search_results_manager.SelectedSearchResultEntry
        if selectedEntry != {}:
            col = row.column()
            col.alignment = 'LEFT'
            col.label(text=selectedEntry.get('displayProperties').get('name'))
            row = col.row(align=True)
            row.alignment = 'LEFT'
            categories = bpy.types.WindowManager.d2ci_search_results_manager.SelectedSearchResultEntry.get('customAttributes').get('categories')
            for cat in categories:
                row.template_icon(icon_value = bpy.types.WindowManager.d2ci_icons.GetIconId(cat), scale=1.5)
            
            ornamentParent = bpy.types.WindowManager.d2ci_search_results_manager.SelectedSearchResultEntry.get('customAttributes').get('ornamentParent') or ''
            if len(ornamentParent) > 0:
                col.label(text=bpy.types.WindowManager.d2ci_search_results_manager.SelectedSearchResultEntry.get('customAttributes').get('ornamentParent'))
            else:
                col.label(text=str(selectedEntry.get('itemTypeDisplayName')))

            row = self.layout.row()
            col.label(text=', '.join(str(x) for x in selectedEntry.get('customAttributes').get('hashList')))

            self.layout.separator(factor=2, type="LINE")
            exportModels = self.layout.row()
            exportModels.operator(UI_OT_D2CI_RunRipperExport.bl_idname, text=UI_OT_D2CI_RunRipperExport.bl_label)
            exportModels.enabled = not ctx.IsRippingExport

            if len(ctx.RippingExportText) != 0:
                row = self.layout.row()
                row.alignment = "RIGHT"
                row.label(text=ctx.RippingExportText)



    def DrawSettings(self, context):
        ctx = context.window_manager.d2ci
        
        # D2 Packages Folder
        row = self.layout.row(align=True)
        row.alignment = "CENTER"
        row.label(text="D2 Package Directory")
        row = self.layout.row()
        row.prop(ctx, "D2PackageFilePath", text="")

        self.layout.separator(factor=2, type="LINE")

        # D2 Output Folder
        row = self.layout.row(align=True)
        row.alignment = "CENTER"
        row.label(text="Output Directory")
        row = self.layout.row()
        row.prop(ctx, "D2OutputFilePath", text="")

        self.layout.separator(factor=2, type="LINE")

        # Number of rows from search results
        row = self.layout.row(align=True)
        refreshButton = row.column()
        refreshButton.prop(ctx, "D2SearchResultsRows")

        self.layout.separator(factor=2, type="LINE")

        # Cache
        row = self.layout.row(align=True)
        saveSettings = row.column()
        saveSettings.label(text="Cache Size: " + str(bpy.types.WindowManager.d2ci_search_results_manager.GetCacheSize()))

        refreshButton = row.column()
        refreshButton.operator(UI_OT_D2CI_ClearCache.bl_idname, text="", icon=UI_OT_D2CI_ClearCache.bl_icon)

        self.layout.separator(factor=2, type="LINE")

        # Save Settings
        row = self.layout.row(align=True)
        saveSettings = row.column()
        saveSettings.operator(UI_OT_D2CI_SaveSettings.bl_idname, text=UI_OT_D2CI_SaveSettings.bl_label)
        saveSettings.enabled = not bpy.types.WindowManager.d2ci_config.IsPopulatingManifestConfig

        refreshButton = row.column()
        refreshButton.operator(UI_OT_D2CI_Reinitialize.bl_idname, text="", icon=UI_OT_D2CI_Reinitialize.bl_icon)
        refreshButton.enabled = len(bpy.types.WindowManager.d2ci_config.GetConfigItem('General','ManifestVersionNumber')) != 0