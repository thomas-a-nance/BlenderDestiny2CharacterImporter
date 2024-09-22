import sqlite3
import re
import json
from ..methods import helpermethods

databaseFileName = 'D2ItemInventory'
tableListToLoad = ['DestinyInventoryItemDefinition']

def QueryManifestByName(manifestName, nameQueryString, rows=4, includeOrnamentsForExotics=True):
    con = sqlite3.connect(helpermethods.GetManifestLocalPath())
    con.create_function("REGEXP", 2, regexp)
    cur = con.cursor()
    try:
        sqlStr = "SELECT id, json, GROUP_CONCAT(json_extract(json, '$.hash')) hashes"
        sqlStr += " from " + manifestName
        sqlStr += " where ("
        sqlStr += " json_extract(json, '$.displayProperties.name') LIKE ?"
        if includeOrnamentsForExotics:
            sqlStr += " or json_extract(json, '$.displayProperties.description') LIKE ?"
        sqlStr += " )"
        sqlStr += " and json_extract(json, '$.itemSubType') != 0"
        sqlStr += " and json_extract(json, '$.displayProperties.hasIcon')"
        sqlStr += " GROUP BY json_extract(json, '$.displayProperties.icon')"
        sqlStr += " limit " + str(rows*8-1)

        cur.execute(sqlStr, ['%'+nameQueryString+'%', '%change the appearance of %'+nameQueryString+'%.'])
        records = cur.fetchall()
        recordsDict = {}
        for record in records:
            recordsDict[record[0]] = json.loads(record[1])
            recordsDict[record[0]]['customAttributes'] = {}
            recordsDict[record[0]].get('customAttributes')['hashList'] = record[2].split(',')
        return recordsDict
    except Exception as e:
        raise e
    finally:
        cur.close()
        con.close()

def regexp(expr, item):
    reg = re.compile(expr, re.IGNORECASE)
    return reg.search(item) is not None

def GetArmorCategoryJsonQueryFilter(warlock=True, titan=True, hunter=True, head=True, arms=True, chest=True, legs=True, classItem=True, shader=True):
    armorClass = []
    armorSubtypes = []
    armorOrnamentsToGet = []
    if warlock:
        armorClass.append("warlock")
    if titan:
        armorClass.append("titan")
    if hunter:
        armorClass.append("hunter")
    if shader:
        armorSubtypes.append("20")
    if head:
        armorSubtypes.append("26")
        armorOrnamentsToGet.append('head')
    if arms:
        armorSubtypes.append("27")
        armorOrnamentsToGet.append('arms')
    if chest:
        armorSubtypes.append("28")
        armorOrnamentsToGet.append('chest')
    if legs:
        armorSubtypes.append("29")
        armorOrnamentsToGet.append('legs')
    if classItem:
        armorSubtypes.append("30")
        armorOrnamentsToGet.append('class')
    
    #$.itemType
    #$.itemSubType
    #$.plug.plugCategoryIdentifier
    armorOrnament = 21
    classSlots = '|'.join(armorClass)
    armorSlots = '|'.join(armorSubtypes)
    armorOrnamentSlots = '|'.join(armorOrnamentsToGet)
    armorShaderFullJson = "\"itemSubType\":(" + armorSlots + ")"
    armorOrnamentFullJson = "\"plugCategoryIdentifier\":\"[a-zA-Z0-9_]*(" + classSlots + ")[a-zA-Z0-9_]*(" + armorOrnamentSlots + ").*\"itemSubType\":" + str(armorOrnament)
    queryString = "((json REGEXP '" + armorShaderFullJson + "') or (json REGEXP '" + armorOrnamentFullJson + "'))"

    return queryString

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

#Sidearm: 17
#Sword: 18
#Mask: 19
#Shader: 20
#Ornament: 21
#FusionRifleLine: 22
#GrenadeLauncher: 23
#SubmachineGun: 24
#TraceRifle: 25
#HelmetArmor: 26
#GauntletsArmor: 27
#ChestArmor: 28
#LegArmor: 29
#ClassArmor: 30
#Bow: 31
#DummyRepeatableBounty: 32
#Glaive: 33