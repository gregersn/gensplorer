import unittest

from gensplorer.services.dna import DNAProvider
from gensplorer.services.dna import utils


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


class TestOverlapp(unittest.TestCase):
    def test_overlapping_segment(self):
        a = {'start': 0, 'end': 100}

        c = {'start': 10, 'end': 120}
        d = {'start': 110, 'end': 150}

        e = {'start': 10, 'end': 50}

        self.assertTrue(utils.segment_overlap(a, c))
        self.assertTrue(utils.segment_overlap(c, a))

        self.assertTrue(utils.segment_overlap(c, d))
        self.assertTrue(utils.segment_overlap(d, c))

        self.assertFalse(utils.segment_overlap(a, d))
        self.assertFalse(utils.segment_overlap(d, a))

        self.assertTrue(utils.segment_overlap(a, e))
        self.assertTrue(utils.segment_overlap(e, a))

    def test_overlapping_chromosome(self):
        a = [{'start': 0, 'end': 20}, {'start': 40,
                                       'end': 60}, {'start': 100, 'end': 200}]
        b = [{'start': 10, 'end': 30}]
        c = [{'start': 10, 'end': 15}, {'start': 65, 'end': 80}]

        d = [{'start': 24, 'end': 30}, {'start': 62, 'end': 95}, {'start': 201, 'end': 250}]

        self.assertTrue(utils.chromosome_overlap(a, b))
        self.assertTrue(utils.chromosome_overlap(b, a))

        self.assertTrue(utils.chromosome_overlap(a, c))
        self.assertTrue(utils.chromosome_overlap(c, a))

        self.assertTrue(utils.chromosome_overlap(c, b))
        self.assertTrue(utils.chromosome_overlap(b, c))

        self.assertFalse(utils.chromosome_overlap(a, d))
        self.assertFalse(utils.chromosome_overlap(d, a))

    def test_overlapping_match(self):
        a = [{'start': 0, 'end': 20}, {'start': 40,
                                       'end': 60}, {'start': 100, 'end': 200}]
        b = [{'start': 10, 'end': 30}]
        c = [{'start': 10, 'end': 15}, {'start': 65, 'end': 80}]

        d = [{'start': 24, 'end': 30}, {'start': 62, 'end': 95}, {'start': 201, 'end': 250}]

        match_a = [{'chromosome': 1, 'segments': a}]
        match_b = [{'chromosome': 2, 'segments': b}]
        match_c = [{'chromosome': 1, 'segments': b}]

        self.assertFalse(utils.match_overlap(match_a, match_b))
        self.assertFalse(utils.match_overlap(match_b, match_a))

        self.assertTrue(utils.match_overlap(match_a, match_c))
        self.assertTrue(utils.match_overlap(match_c, match_a))


