import configparser
import json
import os
from ..methods.helpermethods import *

class ConfigManager():
    config = configparser.ConfigParser()
    configFileName = os.path.join(GetProjectLocalPath(), "config.ini")
    configOptions = '''{
            "General": {
                "ManifestVersionNumber": "",
                "Destiny2PackageFileLocation": "",
                "APINumberOfSearchRows": "4"
            }
        }'''
    
    IsPopulatingManifestConfig = False

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