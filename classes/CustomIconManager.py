import bpy
import os
from ..methods.helpermethods import *

class CustomIconManager():
    IconCollection = {}
    IconDirectory = GetProjectImagePath()

    def __init__(self):
        self.IconCollection = bpy.utils.previews.new()

    def __del__(self):
        bpy.utils.previews.remove(self.IconCollection)

    def GetIconId(self, identifier, extension='.png'):
        if os.path.exists(os.path.join(self.IconDirectory, identifier + extension)):
            return self.GetIcon(identifier, extension).icon_id
        return "QUESTION"

    def GetIcon(self, identifier, extension='.png'):
        if identifier in self.IconCollection:
            return self.IconCollection[identifier]
        
        return self.IconCollection.load(identifier, os.path.join(self.IconDirectory, identifier + extension), "IMAGE")