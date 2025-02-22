from World.Update.UpdatePacketBatch import UpdatePacketBatch
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Object.Constants.UpdateObjectFields import ObjectField, ItemField, UnitField, PlayerField
from World.Character.Constants.CharacterClass import CharacterClass
from Utils.Debug.Logger import Logger
from World.Object.Unit.Player.PlayerManager import PlayerManager


class PlayerSpawn(object):

    SPAWN_FIELDS = [
        # Object fields
        ObjectField.GUID,
        ObjectField.TYPE,
        ObjectField.SCALE_X,

        # Unit fields
        UnitField.HEALTH,
        UnitField.MAXHEALTH,
        UnitField.LEVEL,
        UnitField.FACTIONTEMPLATE,
        UnitField.BYTES_0,
        UnitField.FLAGS,
        UnitField.BOUNDINGRADIUS,
        UnitField.COMBATREACH,
        UnitField.DISPLAYID,
        UnitField.NATIVEDISPLAYID,
        UnitField.STAT0,
        UnitField.STAT1,
        UnitField.STAT2,
        UnitField.STAT3,
        UnitField.STAT4,
        UnitField.RESISTANCE_NORMAL,
        UnitField.BASE_HEALTH,

        # Player fields
        PlayerField.FLAGS,
        PlayerField.BYTES_1,
        PlayerField.BYTES_2,

        PlayerField.VISIBLE_ITEM_1_0,
        PlayerField.VISIBLE_ITEM_2_0,
        PlayerField.VISIBLE_ITEM_3_0,
        PlayerField.VISIBLE_ITEM_4_0,
        PlayerField.VISIBLE_ITEM_5_0,
        PlayerField.VISIBLE_ITEM_6_0,
        PlayerField.VISIBLE_ITEM_7_0,
        PlayerField.VISIBLE_ITEM_8_0,
        PlayerField.VISIBLE_ITEM_9_0,
        PlayerField.VISIBLE_ITEM_10_0,
        PlayerField.VISIBLE_ITEM_11_0,
        PlayerField.VISIBLE_ITEM_12_0,
        PlayerField.VISIBLE_ITEM_13_0,
        PlayerField.VISIBLE_ITEM_14_0,
        PlayerField.VISIBLE_ITEM_15_0,
        PlayerField.VISIBLE_ITEM_16_0,
        PlayerField.VISIBLE_ITEM_17_0,

        PlayerField.INV_SLOT_HEAD,
        PlayerField.INV_SLOT_NECK,
        PlayerField.INV_SLOT_SHOULDERS,
        PlayerField.INV_SLOT_BODY,
        PlayerField.INV_SLOT_CHEST,
        PlayerField.INV_SLOT_WAIST,
        PlayerField.INV_SLOT_LEGS,
        PlayerField.INV_SLOT_FEET,
        PlayerField.INV_SLOT_WRISTS,
        PlayerField.INV_SLOT_HANDS,
        PlayerField.INV_SLOT_FINGER1,
        PlayerField.INV_SLOT_FINGER2,
        PlayerField.INV_SLOT_TRINKET1,
        PlayerField.INV_SLOT_TRINKET2,
        PlayerField.INV_SLOT_BACK,
        PlayerField.INV_SLOT_MAINHAND,
        PlayerField.INV_SLOT_OFFHAND,
        PlayerField.INV_SLOT_RANGED,
        PlayerField.INV_SLOT_TABARD,

        PlayerField.XP,
        PlayerField.NEXT_LEVEL_XP,
        PlayerField.CHARACTER_POINTS1,
        PlayerField.CHARACTER_POINTS2,
        PlayerField.SHIELD_BLOCK,
        PlayerField.EXPLORED_ZONES_1,
        PlayerField.MOD_DAMAGE_NORMAL_DONE_PCT,
        PlayerField.BYTES,
        PlayerField.WATCHED_FACTION_INDEX,
        PlayerField.MAX_LEVEL,
        PlayerField.COINAGE
    ]

    # TODO: also call the ItemManager to spawn items
    ITEM_SPAWN_FIELDS = [
        # Object fields
        ObjectField.GUID,
        ObjectField.TYPE,
        ObjectField.ENTRY,
        ObjectField.SCALE_X,

        # Item fields
        ItemField.OWNER,
        ItemField.CONTAINED,
        ItemField.STACK_COUNT,
        ItemField.MAXDURABILITY,
        ItemField.DURABILITY,
        ItemField.DURATION,
        ItemField.FLAGS,
    ]

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.temp_ref = kwargs.pop('temp_ref', None)

        if self.temp_ref is None:
            raise Exception('[Player Spawn]: temp_ref does not exists')

        self.player = self.temp_ref.player
        self.update_packet_builder = UpdatePacketBatch()
        self._set_player_power()

    async def process(self):
        response = PlayerManager()\
            .set(self.player).prepare().build_update_packet(PlayerSpawn.SPAWN_FIELDS).get_update_packet(build=True)

        return WorldOpCode.SMSG_UPDATE_OBJECT, response

    def _set_player_power(self):
        char_class = CharacterClass(self.player.char_class)

        mana_classes = [
            CharacterClass.HUNTER,
            CharacterClass.WARLOCK,
            CharacterClass.SHAMAN,
            CharacterClass.MAGE,
            CharacterClass.PRIEST,
            CharacterClass.DRUID,
            CharacterClass.PALADIN
        ]

        rage_classes = [
            CharacterClass.WARRIOR
        ]

        energy_classes = [
            CharacterClass.ROGUE
        ]

        if char_class in mana_classes:
            self.SPAWN_FIELDS.append(UnitField.POWER1)
            self.SPAWN_FIELDS.append(UnitField.MAXPOWER1)

        elif char_class in rage_classes:
            self.SPAWN_FIELDS.append(UnitField.POWER2)
            self.SPAWN_FIELDS.append(UnitField.MAXPOWER2)

        elif char_class in energy_classes:
            self.SPAWN_FIELDS.append(UnitField.POWER4)
            self.SPAWN_FIELDS.append(UnitField.MAXPOWER4)
