import unittest
from predds_tracker.templatetags import map_colour


class MapColourTests(unittest.TestCase):
    def testReturnsWhiteWhenValueIsNone(self):
        self.assertEqual(
            map_colour.noKillsColor, map_colour.npc_kill_colour(None)
        )

    def testReturnsWhiteWhenValueIsString(self):
        self.assertEqual(
            map_colour.noKillsColor, map_colour.npc_kill_colour("string")
        )

    def testReturnsWhiteWhenValueIsZero(self):
        self.assertEqual(
            map_colour.noKillsColor, map_colour.npc_kill_colour(0)
        )

    def testDoesNotReturnsWhiteWhenValueIsOne(self):
        self.assertNotEqual(
            map_colour.noKillsColor, map_colour.npc_kill_colour(1)
        )

    def testReturnsThousandKillsColorWhenValueIsOneThousand(self):
        self.assertEqual(
            map_colour.thousandKillsColor, map_colour.npc_kill_colour(1000)
        )

    def testDoesNotReturnThousandKillsColorWhenValueIsOneThousandOne(self):
        self.assertNotEqual(
            map_colour.thousandKillsColor, map_colour.npc_kill_colour(1001)
        )

    def testReturnsMaxKillsColorWhenValueIsFourThousand(self):
        self.assertEqual(
            map_colour.maxKillsColor, map_colour.npc_kill_colour(4000)
        )

    def testReturnsMaxKillsColorWhenValueIsGreaterThanFourThousand(self):
        self.assertEqual(
            map_colour.maxKillsColor, map_colour.npc_kill_colour(4001)
        )
