import bpy
from ..methods import helpermethods
from ..methods import manifest

#region Functions & Enums
def SaveSettings(self, context):
    selectedDestiny2PackagesFolder = context.scene.d2ci.D2PackageFilePath
    selectedPackagePathIsValid = manifest.ValidateDestiny2PackageFolderLocation(selectedDestiny2PackagesFolder)
    if not selectedPackagePathIsValid:
        self.report({"ERROR_INVALID_INPUT"}, "Directory selected is invalid, please select the correct packages directory.")
        return {'CANCELLED'}
    helpermethods.SetConfigItem('General', 'Destiny2PackageFileLocation', selectedDestiny2PackagesFolder)
    manifest.LoadD2Database()
    return {'FINISHED'}

def IsMainPanelOptionAvailable(context, identifier):
    if identifier != 'SETTINGS' and len(helpermethods.GetConfigItem('General','ManifestVersionNumber')) == 0:
        return False
    return True

def MainPanelMenu(context):
    option = context
    #if 'options' not in option.panels:
    #    option.name = 'HardOps Helper'
#
    #    new = option.panels.add()
    #    new.name = 'options'
#
    #    new.operators.add().name = 'Operators'
    #    # new.tool.add().name = 'Tool'

    return option
#endregion

# ------------------------------------------------------------------------
#    Property Group
# ------------------------------------------------------------------------

class VIEW3D_PG_D2CI_Props(bpy.types.PropertyGroup):
    D2PackageFilePath: bpy.props.StringProperty(
        name="D2PackageLocation",
        description="Path to Destiny 2 packages folder",
        default=helpermethods.GetConfigItem('General','Destiny2PackageFileLocation') or "",
        maxlen=1024,
        subtype='DIR_PATH'
    )

class VIEW3d_PG_D2CI_PanelDisplay(bpy.types.PropertyGroup):
    context: bpy.props.EnumProperty(
        name = 'Main Panel',
        description = 'D2CI Main Panel',
        items = [
            ('BAG', 'Build-A-Guardian', 'Build a guardian from Destiny 2 to import into the scene', (helpermethods.PatchSignal + "bag"), 0),
            ('SETTINGS', 'Settings', 'Modify settings for D2CI', "SETTINGS", 1)
        ],
        default = 'BAG'
    )

# ------------------------------------------------------------------------
#    Panel Buttons
# ------------------------------------------------------------------------

class VIEW3D_OT_D2CI_Reinitialize(bpy.types.Operator):
    bl_idname = "view3d.d2ci_reinitialize"
    bl_label = "Reinitialize"
    bl_icon = "TRASH"
    bl_description = "Clears the version number, forcing the manifest to be redownloaded on save"

    def execute(self, context):
        helpermethods.SetConfigItem('General','ManifestVersionNumber','')
        return {'FINISHED'}
    
class VIEW3D_OT_D2CI_SaveSettings(bpy.types.Operator):
    bl_idname = "view3d.d2ci_save_settings"
    bl_label = "Save Settings"
    bl_description = "Downloads the manifest to query data"

    def execute(self, context):
        return SaveSettings(self, context)
    
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
        ctx = context.window_manager.d2ciMainPanel
        col = self.layout.column(align=True)
        row = col.row(align=True)
        row.alignment = 'RIGHT'
        row.scale_x = 2
        row.scale_y = 1.25
        row.prop(MainPanelMenu(ctx), 'context', expand=True, icon_only=True)

        #self.layout.separator(factor=2, type="LINE")

        match ctx.context:
            case "BAG":
                return
            case _:
                row = self.layout.row(align=True)
                row.alignment = "CENTER"
                row.label(text="D2 Package Folder")
                row = self.layout.row()
                row.prop(context.scene.d2ci, "D2PackageFilePath")

                self.layout.separator(factor=2, type="LINE")

                row = self.layout.row(align=True)
                saveSettings = row.column()
                saveSettings.operator(VIEW3D_OT_D2CI_SaveSettings.bl_idname, text=helpermethods.GetConfigItem('Labels','SaveSettings'))

                refreshButton = row.column()
                refreshButton.operator(VIEW3D_OT_D2CI_Reinitialize.bl_idname, text="", icon=VIEW3D_OT_D2CI_Reinitialize.bl_icon)
                refreshButton.enabled = len(helpermethods.GetConfigItem('General','ManifestVersionNumber')) != 0