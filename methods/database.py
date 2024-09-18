import sqlite3
import json
from ..methods import helpermethods

databaseFileName = 'D2ItemInventory'
tableListToLoad = ['DestinyInventoryItemDefinition']

def QueryManifestByName(manifestName, queryString, limit=10):
    con = sqlite3.connect(helpermethods.GetManifestLocalPath())
    cur = con.cursor()
    try:
        sqlStr = "SELECT * from " + manifestName + " where json like '%\"name\":\"" + queryString.replace('"', '\\"') + "%' limit " + str(limit)
        cur.execute(sqlStr)
        records = cur.fetchall()
        recordsDict = {}
        for record in records:
            recordsDict[record[0]] = json.loads(record[1])
        return recordsDict
    except Exception as e:
        raise e
    finally:
        cur.close()
        con.close()

def ConvertDatabaseIdToHash(dbId):
    hash = int(dbId)
    if (hash & (1 << (32 - 1))) != 0:
        hash = hash - (1 << 32)
    return hash

#displayProperties->name = name
#displayProperties->icon = icon
#inventory->tierTypeName = rarity
#inventory->tierType = 0 (Unknown), 1 (Currency), 2 (Basic), 3 (Common), 4 (Rare), 5 (Superior), 6 (Exotic)
#itemTypeDisplayName = item type

#classType: 
    # 0 (Titan), 
    # 1 (Hunter), 
    # 2 (Warlock), 
    # 3 (Unknown)
    #backup: plug.plugCategoryIdentifier.rsplit('_')[2]

#itemSubtype:
#https://bungie-net.github.io/multi/schema_Destiny-DestinyItemSubType.html#schema_Destiny-DestinyItemSubType