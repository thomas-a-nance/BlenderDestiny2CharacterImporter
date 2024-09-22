import configparser
import json
import os
from ..methods.helpermethods import *

class ConfigManager():
    config = configparser.ConfigParser()
    configFileName = os.path.join(GetProjectLocalPath(), "config.ini")
    HasModifiedConfig = False
    configOptions = '''{
            "General": {
                "ManifestVersionNumber": "",
                "Destiny2PackageFileLocation": "",
                "Destiny2OutputFileLocation": "",
                "APINumberOfSearchRows": "4"
            }
        }'''

    def __del__(self):
        self.config = None

    def InitConfig(self):
        self.config.read(self.configFileName)
        configJsonDefaults = json.loads(self.configOptions)
        for category in configJsonDefaults:
            if category not in self.config:
                self.config[category] = {}
            for attribute, value in configJsonDefaults[category].items():
                if attribute not in self.config[category]:
                    self.config[category][attribute] = value

        self.UpdateConfigFile()

    def UpdateConfigFile(self):
        with open(self.configFileName, 'w') as configfile:
            self.config.write(configfile)

    def GetConfigItem(self, category, key):
        self.config.read(self.configFileName)
        if category not in self.config:
            return None
        categoryList = self.config[category]
        
        if not key in categoryList:
            return None
        return categoryList[key]

    def SetConfigItem(self, category, key, value):
        self.config.read(self.configFileName)
        if category not in self.config:
            return None
        categoryList = self.config[category]
        
        if not key in categoryList:
            return None
        categoryList[key] = value
        self.UpdateConfigFile()
        return True
    
    def GetMainPanelDefaultTab(self) -> int:
        if self.ShouldShowAllMainPanelTabs():
            return 0
        else:
            return 1
    
    def GetMainPanelTabsAsEnum(self):
        mainPanels = []
        if self.ShouldShowAllMainPanelTabs():
            mainPanels.append(('BAG', 'Build-A-Guardian', 'Build a guardian from Destiny 2 to import into the scene', bpy.types.WindowManager.d2ci_icons.GetIconId("bag"), 0))

        mainPanels.append(('SETTINGS', 'Settings', 'Modify settings for D2CI', bpy.types.WindowManager.d2ci_icons.GetIconId("settings"), 1))
        return mainPanels
    
    def ShouldShowAllMainPanelTabs(self):
        return len(self.GetConfigItem('General','ManifestVersionNumber')) != 0 \
            and os.path.exists(self.GetConfigItem('General','Destiny2PackageFileLocation')) \
            and len(self.GetConfigItem('General','Destiny2PackageFileLocation')) > 0 \
            and os.path.exists(self.GetConfigItem('General','Destiny2OutputFileLocation')) \
            and len(self.GetConfigItem('General','Destiny2OutputFileLocation')) > 0 \
            and not bpy.types.WindowManager.d2ci_config.HasModifiedConfig