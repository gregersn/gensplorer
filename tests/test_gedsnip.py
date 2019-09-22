import os
import unittest

from gensplorer.services import gedsnip

TEST_GED_FILE = os.path.join(os.getcwd(), "tests", "test.ged")


class TestManipulator(unittest.TestCase):
    def setUp(self):
        self.manipulator = gedsnip.init_manipulator(TEST_GED_FILE)

    def test_init(self):
        self.assertIsNotNone(self.manipulator)
        self.assertEqual(type(self.manipulator), gedsnip.GedcomManipulator)
        self.assertIsNotNone(self.manipulator.gedcom)

    def test_namelist(self):
        namelist = self.manipulator.namelist
        self.assertIsNotNone(namelist)
        self.assertGreater(len(namelist), 0)
