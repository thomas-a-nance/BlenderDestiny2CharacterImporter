import json
import os
import pathlib
import re
import bpy
from mathutils import Matrix

bl_info = {
    "name" : "Destiny 2 Character Importer",
    "author" : "Thomas Nance",
    "description" : "",
    "blender" : (3, 0, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

HexToVertexGroup = [
    ["35B14D1B","Calf.L"],
    ["8BD44A3F","Calf.R"],
    ["038E2D3A","Clav.L"],
    ["A9D76416","Clav.R"],
    ["0F8B505D","Foot.L"],
    ["B9B9E05D","Foot.R"],
    ["897A1504","ForeArm.L"],
    ["A3781DCD","ForeArm.R"],
    ["8C83CB67","Hand.L"],
    ["DE9D6BEA","Hand.R"],
    ["7E92D640","Head"],
    ["512BAB0F","Index_1.L"],
    ["63B2C7F1","Index_1.R"],
    ["522BAB0F","Index_2.L"],
    ["60B2C7F1","Index_2.R"],
    ["532BAB0F","Index_3.L"],
    ["61B2C7F1","Index_3.R"],
    ["B0FB749B","Middle_1.L"],
    ["621DA196","Middle_1.R"],
    ["B3FB749B","Middle_2.L"],
    ["611DA196","Middle_2.R"],
    ["B2FB749B","Middle_3.L"],
    ["601DA196","Middle_3.R"],
    ["0D4EBB10","Neck_1"],
    ["0E4EBB10","Neck_2"],
    ["4A0810C4","Pedestal"],
    ["C7C0BA6E","Pelvis"],
    ["3C17867B","Pinky_1.L"],
    ["C22F2F1F","Pinky_1.R"],
    ["3F17867B","Pinky_2.L"],
    ["C12F2F1F","Pinky_2.R"],
    ["3E17867B","Pinky_3.L"],
    ["C02F2F1F","Pinky_3.R"],
    ["D13A859A","Ring_1.L"],
    ["2F90340E","Ring_1.R"],
    ["D23A859A","Ring_2.L"],
    ["2C90340E","Ring_2.R"],
    ["D33A859A","Ring_3.L"],
    ["2D90340E","Ring_3.R"],
    ["2CDBADE7","Shoulder_Twist_Fixup.L"],
    ["B267287F","Shoulder_Twist_Fixup.R"],
    ["A152A6A2","Spine_1"],
    ["A252A6A2","Spine_2"],
    ["A352A6A2","Spine_3"],
    ["695DAF09","Thigh.L"],
    ["9F0FD28C","Thigh.R"],
    ["8961B2FD","Thumb_1.L"],
    ["03394092","Thumb_1.R"],
    ["8A61B2FD","Thumb_2.L"],
    ["00394092","Thumb_2.R"],
    ["8B61B2FD","Thumb_3.L"],
    ["01394092","Thumb_3.R"],
    ["9D7EE73A","Toe.L"],
    ["6B138432","Toe.R"],
    ["D1232BA2","UpperArm.L"],
    ["17025F50","UpperArm.R"],
    ["52EDE88C","Utility"],
    ["8326E1EA","Wrist_Twist_Fixup.L"],
    ["AD25DDCE","Wrist_Twist_Fixup.R"]
]

def ImportModelsForGuardian(context):
    partPrefix = []
    if(len(context.scene.d2ci.helmetPath) != 0):
        partPrefix += ImportAndModifyFbxForCharacter(context.scene.d2ci.helmetPath,  context.scene.d2ci.isFemale)
    if(len(context.scene.d2ci.gauntletPath) != 0):
        partPrefix += ImportAndModifyFbxForCharacter(context.scene.d2ci.gauntletPath,  context.scene.d2ci.isFemale)
    if(len(context.scene.d2ci.chestPath) != 0):
        partPrefix += ImportAndModifyFbxForCharacter(context.scene.d2ci.chestPath,  context.scene.d2ci.isFemale)
    if(len(context.scene.d2ci.legPath) != 0):
        partPrefix += ImportAndModifyFbxForCharacter(context.scene.d2ci.legPath,  context.scene.d2ci.isFemale)
    if(len(context.scene.d2ci.classPath) != 0):
        partPrefix += ImportAndModifyFbxForCharacter(context.scene.d2ci.classPath,  context.scene.d2ci.isFemale)

    if len(partPrefix) > 0:
        # Skeleton
        skeletonFilePath = str(pathlib.Path(__file__).parent.resolve()) + "\\Resources\\D2 PlayerSkeleton.blend"
        ikCollectionName = ("Female" if context.scene.d2ci.isFemale else "Male") + " IK Rig"
        with bpy.data.libraries.load(skeletonFilePath) as (data_from, data_to):
            data_to.collections += [c for c in data_from.collections if c==ikCollectionName]

        collection = bpy.data.collections.get(ikCollectionName)
        bpy.context.scene.collection.children.link(collection)
        newCollectionName = context.scene.d2ci.guardianName
        if bpy.data.collections.get(newCollectionName) is not None:
            for x in range(1, 1000):
                newCollectionName = context.scene.d2ci.guardianName + f".{x:03d}"
                if bpy.data.collections.get(newCollectionName) is None:
                    break
        collection.name = newCollectionName
        collection.objects[ikCollectionName].name = newCollectionName + "_IK_Rig"

        # Move Objects To New Collection & Rename Vertex Groups
        bpy.ops.object.select_all(action='DESELECT')
        rePrefixString = '^' + "|^".join(re.escape(p) for p in partPrefix)
        objs = [obj for obj in bpy.context.scene.objects if re.match(rePrefixString, obj.name)]
        for obj in objs:
            obj.name = context.scene.d2ci.guardianName + "_" + obj.name
            if obj.name not in collection.objects:
                for col in obj.users_collection:
                    col.objects.unlink(obj)
                collection.objects.link(obj)

            v_groups = obj.vertex_groups
            for n in HexToVertexGroup:
                if n[0] in v_groups:
                    v_groups[n[0]].name = n[1]
            
            obj.select_set(True)

        # Armature Deform Parent
        armature = collection.objects[newCollectionName + "_IK_Rig"]
        armature.select_set(True)

        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.parent_set(type="ARMATURE")

    else:
        print("There were no models imported. Aborting.")

    print("Done.")

    return {'FINISHED'}

# ------------------------------------------------------------------------
#    Helper Functions
# ------------------------------------------------------------------------

def ImportAndModifyFbxForCharacter(filePathForFbx, isFemale):
    bpy.ops.import_scene.fbx(filepath=bpy.path.abspath(filePathForFbx)
            ,use_manual_orientation=True
            ,global_scale=100
            ,axis_up='Z'
            ,axis_forward="-X"
            ,colors_type="SRGB"
    )

    filePath = os.path.dirname(bpy.path.abspath(filePathForFbx))
    fileBaseName = os.path.splitext(os.path.basename(bpy.path.abspath(filePathForFbx)))[0]
    configFilePath = filePath + "\\" + fileBaseName + "_info.cfg"
    configFile = json.load(open(configFilePath))
    modelPrefixToDelete = list(configFile['Parts'].keys())[1 if isFemale else 0]

    # Delete other gender models
    bpy.ops.object.select_all(action='DESELECT')
    DeleteModelsBasedOnPrefixAndArmatures(modelPrefixToDelete, configFile['Parts'].keys())
    ApplyModificationsToModel(configFile['Parts'].keys())

    return list(configFile['Parts'].keys())

def DeleteModelsBasedOnPrefixAndArmatures(modelPrefixToDelete, modelPrefixList, topLevel = True):
    rePrefixString = '^' + "|^".join(re.escape(p) for p in modelPrefixList)
    objs = [obj for obj in bpy.context.scene.objects if re.match(rePrefixString, obj.name)]
    for o in objs:
        if o.name.startswith(modelPrefixToDelete):
            o.select_set(True)
            if o.parent != None:
                DeleteModelsBasedOnPrefixAndArmatures(o.parent.name, modelPrefixList, False)

        FindAndDeleteArmatureParent(o.name)

    if topLevel: 
        for obj in bpy.context.selected_objects:
            if(obj.type == "ARMATURE"):
                bpy.data.armatures.remove(obj.data)
            elif(obj.type == 'MESH'):
                bpy.data.meshes.remove(obj.data)

def FindAndDeleteArmatureParent(modelNameToRecurse):
    o = bpy.context.scene.objects[modelNameToRecurse]
    if o.type == "ARMATURE":
        o.select_set(True) 
    if o.parent != None:
        FindAndDeleteArmatureParent(o.parent.name)
    o.modifiers.clear()

def ApplyModificationsToModel(modelPrefixList):
    rePrefixString = '^' + "|^".join(re.escape(p) for p in modelPrefixList)
    objs = [obj for obj in bpy.context.scene.objects if re.match(rePrefixString, obj.name)]

    materialsToDelete = []

    for o in objs:
        # Rotate -90
        o.rotation_euler = (0,0,-1.5708) 
        mb = o.matrix_basis
        loc, rot, scale = mb.decompose()
        T = Matrix.Translation(loc)
        R = rot.to_matrix().to_4x4()
        S = Matrix.Diagonal(scale).to_4x4()
        if hasattr(o.data, "transform"):
            o.data.transform(R)
        for c in o.children:
            c.matrix_local = R @ c.matrix_local
        o.matrix_basis = T @ S

        # Find Materials To Remove
        materialsToDelete += list(o.data.materials)
        o.data.materials.clear()

        # Clean Up Loose
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.mode_set(mode='OBJECT') 
        if o.type == "MESH":
            bpy.ops.object.mode_set(mode='EDIT')            
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=False)
            bpy.ops.object.mode_set(mode='OBJECT')


        # TODO: Cloth?

        # ???
        

    # Remove Materials
    for m in materialsToDelete:
        bpy.data.materials.remove(m)

# ------------------------------------------------------------------------
#    Panel Properties
# ------------------------------------------------------------------------

class VIEW3D_PT_Destiny2_Character_Importer_Properties(bpy.types.PropertyGroup):
    isFemale: bpy.props.BoolProperty(
        name="Is Female",  
        description="Body type of imported guardian.",
        default = False
    )

    guardianName: bpy.props.StringProperty(
        name="",
        description="Name of collection to put armor in",
        default="Guardian",
        maxlen=1024)

    helmetPath: bpy.props.StringProperty(
        name="",
        description="Path to guardian helmet fbx",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')
    
    gauntletPath: bpy.props.StringProperty(
        name="",
        description="Path to guardian gauntlet fbx",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')
    
    chestPath: bpy.props.StringProperty(
        name="",
        description="Path to guardian chest armor fbx",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')
    
    legPath: bpy.props.StringProperty(
        name="",
        description="Path to guardian leg armor fbx",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')
    
    classPath: bpy.props.StringProperty(
        name="",
        description="Path to guardian class item fbx",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')

# ------------------------------------------------------------------------
#    Panel Functions
# ------------------------------------------------------------------------

class VIEW3D_OT_Destiny2_Character_Importer_Functions(bpy.types.Operator):
    bl_idname = "view3d.destiny2_character_importer_functions"
    bl_label = "Import Models"

    def execute(self, context):
        return ImportModelsForGuardian(context)

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
        row = self.layout.row(align=True)
        row.alignment = "CENTER"
        row.label(text="Gender")
        col = self.layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.d2ci, 'isFemale', text="Male", toggle=True, invert_checkbox=True)
        row.prop(context.scene.d2ci, 'isFemale', text="Female", toggle=True)

        self.layout.separator(factor=4, type="LINE")

        row = self.layout.row(align=True)
        row.alignment = "CENTER"
        row.label(text="Guardian Name")
        row = self.layout.row()
        row.prop(context.scene.d2ci, "guardianName")

        self.layout.separator(factor=4, type="LINE")

        row = self.layout.row(align=True)
        row.alignment = "CENTER"
        row.label(text="Armor")
        row = self.layout.row()
        row.prop(context.scene.d2ci, "helmetPath", text="Helmet")
        row = self.layout.row()
        row.prop(context.scene.d2ci, "gauntletPath", text="Gauntlets")
        row = self.layout.row()
        row.prop(context.scene.d2ci, "chestPath", text="Chest Armor")
        row = self.layout.row()
        row.prop(context.scene.d2ci, "legPath", text="Leg Armor")
        row = self.layout.row()
        row.prop(context.scene.d2ci, "classPath", text="Class Item")

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