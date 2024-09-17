import bpy
from bpy.types import Panel
from .. import bl_info

class D2CI_PT_Button(Panel):
    bl_label = f'''D2CI v{bl_info['version'][0]}.{bl_info['version'][1]}.{bl_info['version'][2]}'''
    bl_space_type = "VIEW_3D"  # 3D Viewport area (find list of values here https://docs.blender.org/api/current/bpy_types_enum_items/space_type_items.html#rna-enum-space-type-items)
    bl_region_type = "UI"  # Sidebar region (find list of values here https://docs.blender.org/api/current/bpy_types_enum_items/region_type_items.html#rna-enum-region-type-items)
    bl_category = "D2CI" # Sidebar name
    bl_label = "Destiny 2 Character Importer" # Panel Title