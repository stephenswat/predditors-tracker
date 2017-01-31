import unittest
from colour import Color
from predds_tracker.templatetags import map_colour


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
