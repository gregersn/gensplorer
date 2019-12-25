#!/usr/bin/env python3

import os
import tempfile
import unittest

from gensplorer.services.dna.match import Matches


class TestPaths(unittest.TestCase):
    def setUp(self):
        self.tempfile = tempfile.NamedTemporaryFile(delete=False)
        self.workdirectory = os.path.dirname(self.tempfile.name)

    def tearDown(self):
        if os.path.isfile(self.tempfile.name):
            os.unlink(self.tempfile.name)

    def test_workdir(self):
        matches = Matches({})
        matches.save(self.tempfile.name)

        self.assertEqual(matches.workingdir,
                         os.path.dirname(self.tempfile.name))

    def test_set_gedcom_in_same_folder(self):
        matches = Matches({})

        matches.gedfile = os.path.join(
            os.path.dirname(self.tempfile.name),
            'test.ged')
        matches.save(self.tempfile.name)

        self.assertEqual(matches.gedfile, 'test.ged')

    def test_set_gedcom_parent(self):
        matches = Matches({})

        matches.gedfile = os.path.abspath(os.path.join(
            os.path.dirname(self.tempfile.name), '..', 'test.ged'))

        matches.save(self.tempfile.name)

        self.assertEqual(matches.gedfile, '../test.ged')

    def test_set_gedom_in_subfolder(self):
        matches = Matches({})
        matches.gedfile = os.path.join(os.path.dirname(
            self.tempfile.name), 'ged', 'test.ged')
        matches.save(self.tempfile.name)
        self.assertEqual(matches.gedfile, 'ged/test.ged')

    def test_set_tester_dna_match_file(self):
        matches = Matches({})
        matches.gedfile = os.path.join(self.workdirectory, "test.ged")

        matches.add_tester("a", "a", ftdna=os.path.join(
            self.workdirectory, "test.csv"),
            myheritage=os.path.join(self.workdirectory, "../test.csv"))

        matches.save(self.tempfile.name)

        a = matches.get_tester("a")
        self.assertEqual(a['shared_segments']['ftdna'],
                         "test.csv")

        self.assertEqual(a['shared_segments']['myheritage'],
                         "../test.csv")
