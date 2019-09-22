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

        self.assertEqual(p3.matches['id1'].matchdata['ftdna'], 'ftdna')
        self.assertEqual(p3.matches['id1'].matchdata['myheritage'], 'myheritage')

        p3.delete()


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


class TestParsers(unittest.TestCase):
    def test_parse_ftdna(self):
        data = """Name,Match Name,Chromosome,Start Location,End Location,Centimorgans,Matching SNPs
John Doe,Jane Doe,1,97361501,98738209,1.74,800
John Doe,Jane Doe,1,225194241,227239975,1.33,500
John Doe,Jane Doe,2,48105815,50978138,2.33,900
"""

        parsed = DNAProvider.parse_overlap_ftdna(data)

        self.assertEqual(parsed['matchname'], "Jane Doe")
        self.assertEqual(parsed['name'], "John Doe")
        self.assertEqual(len(parsed['segments']), 3)
        self.assertEqual(parsed['segments'][0]['centimorgans'], '1.74')
        self.assertEqual(parsed['segments'][1]['centimorgans'], '1.33')
        self.assertEqual(parsed['segments'][2]['snps'], '900')

    def test_parse_myheritage(self):
        data = """Name,Match Name,Chromosome,Start Location,End Location,Start RSID,End RSID,Centimorgans,SNPs
John Doe,Jane Doe,2,84899144,98715864,rs12185616,rs2100272,6.6,2304
John Doe,Jane Doe,4,111195187,118652449,rs7673060,rs10016031,7.1,3328
John Doe,Jane Doe,16,21288101,25694279,rs226039,rs2966227,7.4,2048"""

        parsed = DNAProvider.parse_overlap_myheritage(data)

        self.assertEqual(parsed['matchname'], "Jane Doe")
        self.assertEqual(parsed['name'], "John Doe")
        self.assertEqual(len(parsed['segments']), 3)
        self.assertEqual(parsed['segments'][0]['centimorgans'], '6.6')
        self.assertEqual(parsed['segments'][1]['centimorgans'], '7.1')
        self.assertEqual(parsed['segments'][2]['snps'], '2048')
