import unittest
from colour import Color
from predds_tracker.templatetags import map_colour
from predds_tracker.models import Character


class MapColourTests(unittest.TestCase):
    def testReturnsWhiteWhenValueIsNone(self):
        self.assertEqual(
            Color('white'), map_colour.npc_kill_colour(None)
        )

    def testReturnsWhiteWhenValueIsString(self):
        self.assertEqual(
            Color('white'), map_colour.npc_kill_colour("string")
        )

    def testReturnsWhiteWhenValueIsZero(self):
        self.assertEqual(
            Color('white'), map_colour.npc_kill_colour(0)
        )

    def testReturnsWhiteWhenValueIsOne(self):
        self.assertEqual(
            Color('white'), map_colour.npc_kill_colour(1)
        )

    def testDoesNotReturnsWhiteWhenValueIsTen(self):
        self.assertNotEqual(
            Color('white'), map_colour.npc_kill_colour(10)
        )

    def testReturnsThousandKillsColorWhenValueIsOneThousand(self):
        self.assertEqual(
            Color('#DC4D37'), map_colour.npc_kill_colour(1000)
        )

class CharacterTests(unittest.TestCase):
    def setUp(self):
        self.ccp_cart = Character(id=92025524)
        self.placeholder = Character(id=1206632531, alliance_id=5)
        self.ccp_cart.update_data()
        self.placeholder.update_data()

    def testCharacterCorporationIDIsCorrect(self):
        self.assertEqual(
            self.ccp_cart.corporation_id, 98356193
        )

    def testCharacterAllianceIDIsCorrect(self):
        self.assertEqual(
            self.ccp_cart.alliance_id, 434243723
        )

    def testCharacterAllianceIDIsNull(self):
        self.assertEqual(
            self.placeholder.alliance_id, None
        )
