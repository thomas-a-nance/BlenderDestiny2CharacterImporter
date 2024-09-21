import shutil
import math
import re
from ..methods.helpermethods import *

class SearchResultsManager():
    ResultsCollection = {}
    QueryResults = {}
    SearchResultsDirectory = GetProjectSearchResultsImagePath()
    TempResultDirectory = GetProjectTempImagePath()
    CacheResultDirectory = GetProjectCacheImagePath()
    ProjectImageDirectory = GetProjectImagePath()
    SelectedSearchResultEntry = {}

    def __init__(self):
        self.ResultsCollection = bpy.utils.previews.new()

    def __del__(self):
        bpy.utils.previews.remove(self.ResultsCollection)

    def SetQueryResultsFromSearch(self, results):
        self.QueryResults = results
        self.CopyFilesFromTempToCacheResults()
        self.MoveFilesFromTempToSearchResults()

    def ClearCollectionAndFolder(self):
        self.ResultsCollection.clear()
        self.QueryResults = {}
        self.ClearEnumItem()
        shutil.rmtree(self.SearchResultsDirectory, ignore_errors=True)
        shutil.rmtree(self.TempResultDirectory, ignore_errors=True)
        os.makedirs(self.SearchResultsDirectory, mode=0o777, exist_ok=True)
        os.makedirs(self.TempResultDirectory, mode=0o777, exist_ok=True)
        os.makedirs(self.CacheResultDirectory, mode=0o777, exist_ok=True)

    def ExistsInCache(self, fileName, extension = ".jpg"):
        return os.path.exists(os.path.join(self.CacheResultDirectory, fileName + extension))

    def CopyFileFromCacheToTempResults(self, file, extension = ".jpg"):
        if self.ExistsInCache(file, extension):
            src_path = os.path.join(self.CacheResultDirectory, file + extension)
            dst_path = os.path.join(self.TempResultDirectory, file + extension)
            shutil.copy(src_path, dst_path)

    def CopyFilesFromTempToCacheResults(self):
        allfiles = os.listdir(self.TempResultDirectory)
        for f in allfiles:
            src_path = os.path.join(self.TempResultDirectory, f)
            dst_path = os.path.join(self.CacheResultDirectory, f)
            shutil.copy(src_path, dst_path)

    def MoveFilesFromTempToSearchResults(self):
        allfiles = os.listdir(self.TempResultDirectory)
        for f in allfiles:
            src_path = os.path.join(self.TempResultDirectory, f)
            dst_path = os.path.join(self.SearchResultsDirectory, f)
            shutil.move(src_path, dst_path)
        
    def ClearCache(self):
        shutil.rmtree(self.CacheResultDirectory, ignore_errors=True)

    def GetCacheSize(self):
        cacheDirectory = Path(self.CacheResultDirectory)
        byteSize = sum(f.stat().st_size for f in cacheDirectory.glob('**/*') if f.is_file())

        if byteSize == 0:
            return "0 B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(byteSize, 1024)))
        p = math.pow(1024, i)
        s = round(byteSize / p, 2)
        return "%s %s" % (s, size_name[i])

    def GetCollectionAsEnum(self):
        resultItems = []
        if os.path.exists(self.SearchResultsDirectory) and len(os.listdir(self.SearchResultsDirectory)) > 0:
            for i, name in enumerate(os.listdir(self.SearchResultsDirectory)):
                filepath = os.path.join(self.SearchResultsDirectory, name)
                resultItems.append(self.GetItemForEnum(i+1, name, filepath))

        enumItems = []
        if len(resultItems) == len(self.QueryResults.keys()) and len(resultItems) > 0:
            noneItemId = self.GetImageForEnum("engram", os.path.join(GetProjectImagePath(), "engram.png")).icon_id
            enumItems = [("None", "", "", noneItemId, 0)]
        else:
            enumItems = [("None", "", "", 0, 0)]

        enumItems = enumItems + resultItems
        return enumItems

    def GetImageForEnum(self, name, filepath):
        icon = self.ResultsCollection.get(name)
        if not icon:
            return self.ResultsCollection.load(name, filepath, 'IMAGE')
        else:
            return self.ResultsCollection[name]

    def GetItemForEnum(self, i, name, filepath):
        thumb = self.GetImageForEnum(name, filepath)
        try:
            displayName = name
            itemId = int(Path(name).stem)
            if itemId in self.QueryResults.keys():
                displayName = self.QueryResults.get(itemId).get('displayProperties').get('name')

            return (str(itemId), displayName, "", thumb.icon_id, i+1)
        except:
            return (name, name, "", thumb.icon_id, i+1)
        
    def SelectEnumItem(self, value):
        if value in self.QueryResults.keys():
            self.SelectedSearchResultEntry = self.QueryResults.get(value)
            self.SelectedSearchResultEntry['customAttributes'] = {}
            self.SelectedSearchResultEntry.get('customAttributes')['categories'] = self.GetCategoryForSelected()
            self.SelectedSearchResultEntry.get('customAttributes')['ornamentParent'] = ''
            self.SelectedSearchResultEntry.get('customAttributes')['class'] = ''
            
            if 'ornament' in self.SelectedSearchResultEntry.get('customAttributes').get('categories'):
                self.SelectedSearchResultEntry.get('customAttributes')['ornamentParent'] = self.CheckForOrnamentParent()
            className = self.CheckForClassCategory()
            if len(className) > 0:
                self.SelectedSearchResultEntry.get('customAttributes')['class'] = className

    def ClearEnumItem(self):
        self.SelectedSearchResultEntry = {}

    def GetCategoryForSelected(self):
        categories = []
        classCat = self.CheckForClassCategory()
        if len(classCat) > 0:
            categories.append(classCat)

        match self.SelectedSearchResultEntry.get("itemSubType"):
            case 20:
                categories.append('shader')
            case 21:
                categories.append('ornament')
                categories.append(self.CheckForOrnamentCategory())
            case 26:
                categories.append('head')
            case 27:
                categories.append('arms')
            case 28:
                categories.append('chest')
            case 29:
                categories.append('legs')
            case 30:
                categories.append('class')

        return categories
    
    def CheckForClassCategory(self):
        classType = self.SelectedSearchResultEntry.get("classType")
        if classType == 0:
            return "titan"
        if classType == 1:
            return "hunter"
        if classType == 2:
            return "warlock"
        
        #Fallback
        try:
            plugString = self.SelectedSearchResultEntry.get("plug").get('plugCategoryIdentifier')
            if "warlock" in plugString:
                return "warlock"
            if "titan" in plugString:
                return "titan"
            if "hunter" in plugString:
                return "hunter"
        except:
            return ''

    def CheckForOrnamentCategory(self):
        try:
            plugString = self.SelectedSearchResultEntry.get("plug").get('plugCategoryIdentifier')
            regexQuery = re.search("[a-zA-Z0-9_]*(warlock|titan|hunter)[a-zA-Z0-9_]*(head|arms|chest|legs|class)",plugString)
            return regexQuery.group(2)
        except:
            return ''
    
    def CheckForOrnamentParent(self):
        try:
            desc = self.SelectedSearchResultEntry.get('displayProperties').get('description')
            regexQuery = re.search('change the appearance of ([^\.]*)',desc)
            return regexQuery.group(1)
        except:
            return ''
    