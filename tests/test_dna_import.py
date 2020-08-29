import os
import unittest
import tempfile
import shutil
from gensplorer.services import dna
from gensplorer.services.dna.match import Match


class TestImport(unittest.TestCase):
    def setUp(self):
        self.datafolder = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.datafolder)

        if os.path.isfile('./matches_testprofile.json'):
            os.unlink("./matches_testprofile.json")

    def test_ftdna_import(self):
        profile = dna.Profile('testprofile', self.datafolder)
        profile.import_matches(dna.DNAProvider.ftdna, os.path.dirname(
            __file__) + '/ftdna_test_set_1.csv')
        self.assertEqual(profile.matchcount, 4)

        match_a: Match = profile.matches[0]

        self.assertEqual(match_a.name, "Marcus")
        self.assertIn('1', match_a.matchdata['ftdna'])

    def test_myheritage_import(self):
        profile = dna.Profile('testprofile', self.datafolder)
        profile.import_matches(dna.DNAProvider.myheritage, os.path.dirname(
            __file__) + '/myheritage_test_set_1.csv')
        self.assertEqual(profile.matchcount, 5)

    def test_both_imports(self):
        profile = dna.Profile('testprofile', self.datafolder)
        profile.import_matches(dna.DNAProvider.ftdna, os.path.dirname(
            __file__) + '/ftdna_test_set_1.csv')
        profile.import_matches(dna.DNAProvider.myheritage, os.path.dirname(
            __file__) + '/myheritage_test_set_1.csv')
        self.assertEqual(profile.matchcount, 9)

    def test_update_import(self):
        profile = dna.Profile('testprofile', self.datafolder)
        profile.import_matches(dna.DNAProvider.ftdna, os.path.dirname(
            __file__) + '/ftdna_test_set_1.csv')
        profile.import_matches(dna.DNAProvider.ftdna, os.path.dirname(
            __file__) + '/ftdna_test_set_2.csv')
        self.assertEqual(profile.matchcount, 6)
