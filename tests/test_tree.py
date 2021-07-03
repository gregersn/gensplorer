import os
import unittest

from gensplorer.services import tree

TEST_GED_FILE = os.path.join(os.getcwd(), "tests", "test.ged")


class TestTree(unittest.TestCase):
    def setUp(self):
        self.tree = tree.Tree(TEST_GED_FILE)

    def test_build_tree(self):
        self.assertEqual(len(self.tree.individuals.keys()), 0)
        self.assertEqual(len(self.tree.families.keys()), 0)

        self.tree.build_tree()

        self.assertEqual(len(self.tree.individuals.keys()), 19)
        self.assertEqual(len(self.tree.families.keys()), 8)

    def test_find_parents(self):
        self.tree.build_tree()

        samantha = self.tree.individuals['@I4585@']

        parents = samantha.get_parents()

        self.assertEqual(len(parents), 2)

        self.assertIn('@I4580@', parents)
        self.assertIn('@I4584@', parents)

    def test_find_children(self):
        self.tree.build_tree()