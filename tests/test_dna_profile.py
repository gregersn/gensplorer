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

    def test_load_and_save_with_match_edit(self):
        profilename = 'load_and_save_with_match_edit'
        p = Profile(profilename, '.')
        match = Match('id1')
        p.add_match(match)
        p.add_matchdata('id1', DNAProvider.ftdna, 'ftdna')
        p.save()

        p2 = Profile.load(profilename)
        p2.add_matchdata('id1', DNAProvider.myheritage, 'myheritage')
        p2.save(overwrite=True)

        p3 = Profile.load(profilename)

        self.assertEqual(p3.find_match('id1').matchdata['ftdna'], 'ftdna')
        self.assertEqual(p3.find_match(
            'id1').matchdata['myheritage'], 'myheritage')

        p3.delete()
