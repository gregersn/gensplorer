import unittest

from gensplorer.services.dna import Profile


class TestProfile(unittest.TestCase):
    def test_load_and_save(self):
        p = Profile('@I0000@', '.')
        p.save()

        p2 = Profile.load('@I0000@', '.')

        self.assertEqual(p, p2)

        p3 = Profile('@I0001@', '.')
        self.assertNotEqual(p, p3)

        p.delete()
