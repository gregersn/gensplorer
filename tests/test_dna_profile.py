import shutil
import tempfile
import unittest
import os


from gensplorer.services.dna.profile import Profile
from gensplorer.services.dna.match import Match
from gensplorer.services.dna.provider import DNAProvider


class TestProfile(unittest.TestCase):
    def setUp(self):
        self.datafolder = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.datafolder)

    def test_load_and_save(self):
        p = Profile('load_and_save_1', self.datafolder)
        p.save()
        p2 = Profile.load('load_and_save_1', self.datafolder)

        self.assertEqual(p, p2)

        p3 = Profile('load_and_save_2', self.datafolder)
        self.assertNotEqual(p, p3)

        p.delete()

    def test_load_and_save_with_match(self):
        p = Profile('load_and_save_with_match', self.datafolder)
        match = Match('@I0002')
        match.add_matchdata(DNAProvider.ftdna, '1234567')
        p.add_match(match)
        p.save()

        p2 = Profile.load('load_and_save_with_match', self.datafolder)

        self.assertEqual(p, p2)

        p.delete()

    def test_load_and_save_with_match_edit(self):
        profilename = 'load_and_save_with_match_edit'
        p = Profile(profilename, self.datafolder)
        match = Match('id1')
        p.add_match(match)
        p.add_matchdata('id1', DNAProvider.ftdna, 'ftdna')
        p.save()

        p2 = Profile.load(profilename, self.datafolder)
        p2.add_matchdata('id1', DNAProvider.myheritage, 'myheritage')
        p2.save(overwrite=True)

        p3 = Profile.load(profilename, self.datafolder)

        self.assertEqual(p3.find_match('id1').matchdata['ftdna'], 'ftdna')
        self.assertEqual(p3.find_match(
            'id1').matchdata['myheritage'], 'myheritage')

        p3.delete()
    
    def test_find_match(self):
        profile = Profile('testprofile', self.datafolder)
        profile.import_matches(DNAProvider.ftdna, os.path.dirname(__file__) + '/ftdna_test_set_3.csv')

        self.assertEqual(profile.matchcount, 3)

        match_a: Match = profile.find_match(name="A B")
        match_b: Match = profile.find_match(name="C D")
        match_c: Match = profile.find_match(name="E F")

        self.assertEqual(match_a.name, "A B")
        self.assertEqual(match_b.name, "C D")
        self.assertEqual(match_c.name, "E F")
        
        

