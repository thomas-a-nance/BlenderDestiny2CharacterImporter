import bpy
from ..methods import helpermethods
from ..methods import manifest

# ------------------------------------------------------------------------
#    Panel UI
# ------------------------------------------------------------------------
class VIEW3D_PT_Destiny2_Character_Importer(bpy.types.Panel):  # class naming convention ‘CATEGORY_PT_name’
    #Blender Init
    bl_space_type = "VIEW_3D"  # 3D Viewport area (find list of values here https://docs.blender.org/api/current/bpy_types_enum_items/space_type_items.html#rna-enum-space-type-items)
    bl_region_type = "UI"  # Sidebar region (find list of values here https://docs.blender.org/api/current/bpy_types_enum_items/region_type_items.html#rna-enum-region-type-items)
    bl_category = "D2CI" # Sidebar name
    bl_label = "Destiny 2 Character Importer" # Panel Title

    def draw(self, context):
        #row = self.layout.row(align=True)
        #row.alignment = "CENTER"
        #row.label(text="Gender")
        #col = self.layout.column(align=True)
        #row = col.row(align=True)
        #row.prop(context.scene.d2ci, 'isFemale', text="Male", toggle=True, invert_checkbox=True)
        #row.prop(context.scene.d2ci, 'isFemale', text="Female", toggle=True)

        #self.layout.separator(factor=4, type="LINE")

        #row = self.layout.row(align=True)
        #row.alignment = "CENTER"
        #row.label(text="Guardian Name")
        #row = self.layout.row()
        #row.prop(context.scene.d2ci, "guardianName")

        #self.layout.separator(factor=4, type="LINE")

        #row = self.layout.row(align=True)
        #row.alignment = "CENTER"
        #row.label(text="Armor")
        #row = self.layout.row()
        #row.prop(context.scene.d2ci, "helmetPath", text="Helmet")
        #row = self.layout.row()
        #row.prop(context.scene.d2ci, "gauntletPath", text="Gauntlets")
        #row = self.layout.row()
        #row.prop(context.scene.d2ci, "chestPath", text="Chest Armor")
        #row = self.layout.row()
        #row.prop(context.scene.d2ci, "legPath", text="Leg Armor")
        #row = self.layout.row()
        #row.prop(context.scene.d2ci, "classPath", text="Class Item")

        #self.layout.separator(factor=4, type="LINE") 

        row = self.layout.row(align=True)
        row.alignment = "CENTER"
        row.label(text="D2 Package Folder")
        row = self.layout.row()
        row.prop(context.scene.d2ci, "D2PackageFilePath")

        self.layout.separator(factor=4, type="LINE")

        row = self.layout.row(align=True)
        saveSettings = row.column()
        saveSettings.operator(VIEW3D_OT_Destiny2_Character_Importer_InitializeDatabase.bl_idname, text=helpermethods.GetConfigItem('Labels','SaveSettings'))

        refreshButton = row.column()
        refreshButton.operator(VIEW3D_OT_Destiny2_Character_Importer_DatabaseRefresh.bl_idname, text="", icon=VIEW3D_OT_Destiny2_Character_Importer_DatabaseRefresh.bl_icon)
        refreshButton.enabled = len(helpermethods.GetConfigItem('General','ManifestVersionNumber')) != 0

# ------------------------------------------------------------------------
#    Property Group
# ------------------------------------------------------------------------

class VIEW3D_PT_Destiny2_Character_Importer_Properties(bpy.types.PropertyGroup):
    D2PackageFilePath: bpy.props.StringProperty(
        name="",
        description="Path to Destiny 2 packages folder",
        default=helpermethods.GetConfigItem('General','Destiny2PackageFileLocation') or "",
        maxlen=1024,
        subtype='DIR_PATH')

# ------------------------------------------------------------------------
#    Panel Buttons
# ------------------------------------------------------------------------

class VIEW3D_OT_Destiny2_Character_Importer_DatabaseRefresh(bpy.types.Operator):
    bl_idname = "view3d.destiny2_character_importer_database_refresh"
    bl_label = "Reinitialize Database Files"
    bl_icon = "TRASH "

    def execute(self, context):
        helpermethods.SetConfigItem('General','ManifestVersionNumber','')
        return {'FINISHED'}
    
class VIEW3D_OT_Destiny2_Character_Importer_InitializeDatabase(bpy.types.Operator):
    bl_idname = "view3d.destiny2_character_importer_initialize_database"
    bl_label = "Save Settings"

    def execute(self, context):
        return SaveSettings(self, context)
    
# ------------------------------------------------------------------------
#    Panel Functions
# ------------------------------------------------------------------------

def SaveSettings(self, context):
    selectedDestiny2PackagesFolder = context.scene.d2ci.D2PackageFilePath
    selectedPackagePathIsValid = manifest.ValidateDestiny2PackageFolderLocation(selectedDestiny2PackagesFolder)
    if not selectedPackagePathIsValid:
        self.report({"ERROR_INVALID_INPUT"}, "Directory selected is invalid, please select the correct packages directory.")
        return {'CANCELLED'}
    helpermethods.SetConfigItem('General', 'Destiny2PackageFileLocation', selectedDestiny2PackagesFolder)
    manifest.LoadD2Database()
    return {'FINISHED'}