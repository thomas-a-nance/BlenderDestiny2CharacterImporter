from ctypes import *

class DestinyItemInventoryBlockDefinition:
    StackUniqueLabel: str
    MaxStackSize: c_long
    BucketTypeHash: c_uint
    RecoveryBucketTypeHash: c_uint
    TierTypeHash: c_uint
    IsInstanceItem: bool
    TierTypeName: str
    #TierType: TierType
    ExpirationTooltip: str
    ExpiredInActivityMessage: str
    ExpiredInOrbitMessage: str
    SuppressExpirationWhenObjectivesComplete: bool
    RecipeItemHash: c_uint