import unittest

from gensplorer.services.dna import Profile, Match, DNAProvider


class TestProfile(unittest.TestCase):
    def test_load_and_save(self):
        p = Profile('load_and_save_1', '.')
        p.save()
        p2 = Profile.load('load_and_save_1', '.')

        self.assertEqual(p, p2)

        p3 = Profile('load_and_save_2', '.')
        self.assertNotEqual(p, p3)

        p.delete()

    def test_load_and_save_with_match(self):
        p = Profile('load_and_save_with_match', '.')
        match = Match('@I0002')
        match.add_matchdata(DNAProvider.ftdna, '1234567')
        p.add_match(match)
        p.save()

        p2 = Profile.load('load_and_save_with_match')

        self.assertEqual(p, p2)

        p.delete()


class TestMatches(unittest.TestCase):
    def setUp(self):
        self.profile = Profile('@testmatches@', '.')

    def tearDown(self):
        self.profile.delete()

    def test_add_match(self):
        match = Match('@I0002')
        match.add_matchdata(DNAProvider.ftdna, "dummydata")
        self.profile.add_match(match)

        self.assertIn('@I0002', self.profile.matches)
        self.assertEqual(self.profile.matchcount,
                         1, self.profile.matches.keys())

    def test_add_multiple_matches(self):
        match = Match('matcha')
        match.add_matchdata(DNAProvider.ftdna, "dasdfasd")
        self.profile.add_match(match)

        match2 = Match('matchb')
        match2.add_matchdata(DNAProvider.myheritage, "asldkfjasd")
        self.profile.add_match(match2)

        self.assertIn('matcha', self.profile.matches)
        self.assertIn('matchb', self.profile.matches)
        self.assertEqual(self.profile.matchcount,
                         2, self.profile.matches.keys())

    def test_add_more_to_match(self):
        match = Match('matcha')
        match.add_matchdata(DNAProvider.ftdna, '1234567')
        self.profile.add_match(match)

        self.assertEqual(self.profile.matchcount, 1)

        self.profile.add_matchdata('matcha', DNAProvider.myheritage, '7654321')

        self.assertEqual(self.profile.matchcount, 1)

        match = self.profile.matches['matcha']
        self.assertEqual(match.matchdata[DNAProvider.ftdna], '1234567')
        self.assertEqual(match.matchdata[DNAProvider.myheritage], '7654321')
