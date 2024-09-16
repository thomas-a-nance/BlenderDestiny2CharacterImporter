import bpy
import configparser
import json
import requests
import shutil
import asyncio
import gzip
import tempfile
import os

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

config = configparser.ConfigParser()
baseUrl = 'https://bungie.net'
configFileName = os.path.join(tempfile.gettempdir(), "BlenderD2CI", "config.ini")
asyncio.set_event_loop(asyncio.new_event_loop())

def SaveSettings(self, context):
    CreateConfig()
    config.read(configFileName)
    selectedDestiny2PackagesFolder = context.scene.d2ci.D2PackageFilePath
    selectedPackagePathIsValid = ValidateDestiny2PackageFolderLocation(selectedDestiny2PackagesFolder)
    if not selectedPackagePathIsValid:
        self.report({"ERROR_INVALID_INPUT"}, "Directory selected is invalid, please select the correct packages directory.")
        return {'CANCELLED'}
    config['General']['Destiny2PackageFileLocation'] = selectedDestiny2PackagesFolder
    
    loop = getAsyncioLoop()
    d2ManifestQuery = loop.run_until_complete(GetDestiny2Manifest(loop))
    d2Manifest = d2ManifestQuery.json()
    d2ManifestVersion = d2Manifest["Response"]["version"]
    d2ItemDefinitionURL = baseUrl + d2Manifest["Response"]["jsonWorldComponentContentPaths"]["en"]["DestinyInventoryItemDefinition"]
    folderPath = os.path.join(tempfile.gettempdir(), "BlenderD2CI", "Destiny2ItemDefinition")
    jsonFileName = d2ItemDefinitionURL.rsplit('/', 1)[-1]
    fullPathToGzippedJson = os.path.join(folderPath, jsonFileName + ".gz")
    if os.path.exists(os.path.join(folderPath, "download_in_progress")) or not os.path.exists(fullPathToGzippedJson):
        loop.run_until_complete(RedownloadGzippedJson(d2ItemDefinitionURL, folderPath, jsonFileName))

    if config['General']['ManifestVersionNumber'] != d2ManifestVersion:
        if not os.path.exists(fullPathToGzippedJson):
            loop.run_until_complete(RedownloadGzippedJson(d2ItemDefinitionURL, folderPath, jsonFileName))
 
    config['General']['ManifestVersionNumber'] = d2ManifestVersion
    UpdateConfig()
    return {'FINISHED'}

# ------------------------------------------------------------------------
#    Helper Functions
# ------------------------------------------------------------------------

def getAsyncioLoop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        return asyncio.get_event_loop()

def ValidateDestiny2PackageFolderLocation(folderPath):
    if(folderPath != config['General']['Destiny2PackageFileLocation']):
        return any(fname.endswith('.pkg') for fname in os.listdir(folderPath))
    return True

async def GetDestiny2Manifest(loop):
    apiUrl = baseUrl + '/Platform/Destiny2/Manifest/'
    headers = {"Content-Type":"application/json", "X-API-KEY":"aa5aaca04c2d433f923e3cca8119dddf"}
    returnData = requests.get(apiUrl, headers=headers, timeout=None, stream=True)
    return returnData

async def RedownloadGzippedJson(d2ItemDefinitionURL, folderPath, jsonFileName):
    downloadIndicator = os.path.join(folderPath, 'download_in_progress')
    shutil.rmtree(folderPath, ignore_errors=True)
    os.makedirs(folderPath, mode=0o777, exist_ok=True)
    open(downloadIndicator, 'a').close()
    headers = {"X-API-KEY":"aa5aaca04c2d433f923e3cca8119dddf"}

    with requests.get(d2ItemDefinitionURL, headers=headers, timeout=None, stream=True) as response:
        response.raise_for_status()
        with gzip.open(os.path.join(folderPath, jsonFileName + ".gz"), 'wb') as compressedFile:
            for chunk in response.iter_content(chunk_size=8192):
                compressedFile.write(chunk)

    os.remove(downloadIndicator)
    return

def CreateConfig():
    folderPath = os.path.join(tempfile.gettempdir())
    if(not(os.path.exists(os.path.join(folderPath,configFileName)))):
        config.read(configFileName)
        config["General"] = {
            "ManifestVersionNumber": "",
            "Destiny2PackageFileLocation": ""

        }
        UpdateConfig()

def UpdateConfig():
    with open(configFileName, 'w') as configfile:
        config.write(configfile)

# ------------------------------------------------------------------------
#    Panel Properties
# ------------------------------------------------------------------------

class VIEW3D_PT_Destiny2_Character_Importer_Properties(bpy.types.PropertyGroup):
    CreateConfig()
    config.read(configFileName)

    D2PackageFilePath: bpy.props.StringProperty(
        name="",
        description="Path to Destiny 2 packages folder",
        default=config['General']['Destiny2PackageFileLocation'],
        maxlen=1024,
        subtype='DIR_PATH')

# ------------------------------------------------------------------------
#    Panel Functions
# ------------------------------------------------------------------------

class VIEW3D_OT_Destiny2_Character_Importer_Functions(bpy.types.Operator):
    bl_idname = "view3d.destiny2_character_importer_functions"
    bl_label = "Save Settings"

    def execute(self, context):
        return SaveSettings(self, context)

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



        self.layout.separator(factor=4, type="LINE")

        row = self.layout.row(align=True)
        row.operator(VIEW3D_OT_Destiny2_Character_Importer_Functions.bl_idname)

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

from . import auto_load
auto_load.init()

classes = (
    VIEW3D_PT_Destiny2_Character_Importer_Properties,
    VIEW3D_OT_Destiny2_Character_Importer_Functions,
    VIEW3D_PT_Destiny2_Character_Importer
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.d2ci = bpy.props.PointerProperty(type=VIEW3D_PT_Destiny2_Character_Importer_Properties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.d2ci