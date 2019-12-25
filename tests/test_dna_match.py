import os
import unittest
import tempfile
import shutil

from gensplorer.services.dna.profile import Profile
from gensplorer.services.dna.match import Match
from gensplorer.services.dna.provider import DNAProvider


class TestMatches(unittest.TestCase):
    def setUp(self):
        self.datafolder = tempfile.mkdtemp() 
        self.profile = Profile('@testmatches@', self.datafolder)

    def tearDown(self):
        self.profile.delete()
        shutil.rmtree(self.datafolder)

    def test_add_match(self):
        match = Match('@I0002')
        match.add_matchdata(DNAProvider.ftdna, "dummydata")
        self.profile.add_match(match)

        self.assertIsNotNone(self.profile.find_match('@I0002'))
        self.assertEqual(self.profile.matchcount,
                         1, self.profile.matches)

    def test_add_multiple_matches(self):
        match = Match('matcha')
        match.add_matchdata(DNAProvider.ftdna, "dasdfasd")
        self.profile.add_match(match)

        match2 = Match('matchb')
        match2.add_matchdata(DNAProvider.myheritage, "asldkfjasd")
        self.profile.add_match(match2)

        self.assertIsNotNone(self.profile.find_match(
            'matcha'), self.profile.matches)
        self.assertIsNotNone(self.profile.find_match(
            'matchb'), self.profile.matches)
        self.assertEqual(self.profile.matchcount,
                         2)

    def test_add_more_to_match(self):
        match = Match('matcha')
        match.add_matchdata(DNAProvider.ftdna, '1234567')
        self.profile.add_match(match)

        self.assertEqual(self.profile.matchcount, 1)

        self.profile.add_matchdata('matcha', DNAProvider.myheritage, '7654321')

        self.assertEqual(self.profile.matchcount, 1)

        match = self.profile.find_match('matcha')
        self.assertEqual(match.matchdata[DNAProvider.ftdna], '1234567')
        self.assertEqual(match.matchdata[DNAProvider.myheritage], '7654321')

    def test_match_overlap(self):
        profile = Profile('testprofile', self.datafolder)
        profile.import_matches(DNAProvider.ftdna, os.path.dirname(__file__) + '/ftdna_test_set_3.csv')

        self.assertEqual(profile.matchcount, 3)

        match_a: Match = profile.find_match(name="A B")
        match_b: Match = profile.find_match(name="C D")
        match_c: Match = profile.find_match(name="E F")

        self.assertTrue(match_a.matches(match_b))
        self.assertTrue(match_b.matches(match_a))

        self.assertFalse(match_a.matches(match_c))
        self.assertFalse(match_c.matches(match_a))

        self.assertFalse(match_b.matches(match_c))
        self.assertFalse(match_c.matches(match_b))
