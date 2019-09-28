import unittest

from gensplorer.services.dna import Profile, Match, DNAProvider


class TestMatches(unittest.TestCase):
    def setUp(self):
        self.profile = Profile('@testmatches@', '.')

    def tearDown(self):
        self.profile.delete()

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
