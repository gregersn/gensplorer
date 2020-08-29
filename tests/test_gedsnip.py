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

    def test_get_individual(self):
        a = self.manipulator.get_individual("@I4580@")
        self.assertIsNotNone(a)
    
    def test_search_children(self):
        a = self.manipulator.get_individual("@I4580@")
        b = self.manipulator.get_individual("@I4588@")
        namelist = self.manipulator.search_children(a, b)
        self.assertEqual(len(namelist), 3)

    def test_search_siblings(self):
        a = self.manipulator.get_individual("@I1@")
        b = self.manipulator.get_individual("@I4585@")
        namelist = self.manipulator.search_children(a, b)
        self.assertEqual(len(namelist), 3)

    def test_search(self):
        a = self.manipulator.get_individual("@I4580@")
        b = self.manipulator.get_individual("@I4588@")
        namelist = self.manipulator.search(a, b)
        self.assertEqual(len(namelist), 3)
