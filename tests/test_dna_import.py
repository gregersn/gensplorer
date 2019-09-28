import os
import unittest
from gensplorer.services import dna


class TestImport(unittest.TestCase):
    def tearDown(self):
        if os.path.isfile('./matches_testprofile.json'):
            os.unlink("./matches_testprofile.json")

    def test_ftdna_import(self):
        profile = dna.Profile('testprofile', '.')
        profile.import_matches(dna.DNAProvider.ftdna, os.path.dirname(__file__) + '/ftdna_test_set_1.csv')
        self.assertEqual(profile.matchcount, 4)

    def test_myheritage_import(self):
        profile = dna.Profile('testprofile', '.')
        profile.import_matches(dna.DNAProvider.myheritage, os.path.dirname(__file__) + '/myheritage_test_set_1.csv')
        self.assertEqual(profile.matchcount, 5)

    def test_both_imports(self):
        profile = dna.Profile('testprofile', '.')
        profile.import_matches(dna.DNAProvider.ftdna, os.path.dirname(__file__) + '/ftdna_test_set_1.csv')
        profile.import_matches(dna.DNAProvider.myheritage, os.path.dirname(__file__) + '/myheritage_test_set_1.csv')
        self.assertEqual(profile.matchcount, 9)

    def test_update_import(self):
        profile = dna.Profile('testprofile', '.')
        profile.import_matches(dna.DNAProvider.ftdna, os.path.dirname(__file__) + '/ftdna_test_set_1.csv')
        profile.import_matches(dna.DNAProvider.ftdna, os.path.dirname(__file__) + '/ftdna_test_set_2.csv')
        self.assertEqual(profile.matchcount, 6)
