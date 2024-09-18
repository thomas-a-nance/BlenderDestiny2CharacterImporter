import bpy
from .Operators import *
    
# ------------------------------------------------------------------------
#    Panel UI
# ------------------------------------------------------------------------
class VIEW3D_PT_D2CI(bpy.types.Panel):  # class naming convention ‘CATEGORY_PT_name’
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
        
        if len(bpy.types.WindowManager.d2ci_config.GetConfigItem('General','ManifestVersionNumber')) != 0:
            row.prop(MainPanelMenu(ctx), 'MainPanelEnum', expand=True, icon_only=True)
        else:
            ctx.MainPanelEnum = "SETTINGS"
        
        match ctx.MainPanelEnum:
            case "BAG":
                row = self.layout.row(align=True)
                row.alignment = "CENTER"
                row.label(text="API Search")
                row = self.layout.row(align=True)
                row.column()
                row.prop(ctx, "D2APISearchBar", text="")
                searchButton = row.column()
                searchButton.operator(VIEW3D_OT_D2CI_SearchAPI.bl_idname, text="", icon=VIEW3D_OT_D2CI_SearchAPI.bl_icon)
                self.layout.separator(factor=2, type="LINE")
            case _:
                row = self.layout.row(align=True)
                row.alignment = "CENTER"
                row.label(text="D2 Package Folder")
                row = self.layout.row()
                row.prop(ctx, "D2PackageFilePath", text="")

                self.layout.separator(factor=2, type="LINE")

                row = self.layout.row(align=True)
                saveSettings = row.column()
                saveSettings.operator(VIEW3D_OT_D2CI_SaveSettings.bl_idname, text=VIEW3D_OT_D2CI_SaveSettings.bl_label)

                refreshButton = row.column()
                refreshButton.operator(VIEW3D_OT_D2CI_Reinitialize.bl_idname, text="", icon=VIEW3D_OT_D2CI_Reinitialize.bl_icon)
                refreshButton.enabled = len(bpy.types.WindowManager.d2ci_config.GetConfigItem('General','ManifestVersionNumber')) != 0
                return