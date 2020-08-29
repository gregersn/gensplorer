import unittest


from gensplorer.services.project import Project


class TestProject(unittest.TestCase):
    def setUp(self):
        self.project = Project("./tests/test_project.json")

    def test_read_project(self):
        project = Project("./tests/test_project.json")

        self.assertEqual(len(project.testers), 1)
        self.assertEqual(project.gedfile, "test.ged")

    def test_get_tester(self):
        tester = self.project['cassandra']
        self.assertEqual(tester.xref, "I4588")

    def test_matches(self):
        tester = self.project['cassandra']
        self.assertEqual(len(tester.matches), 1)

    def test_get_match(self):
        tester = self.project['cassandra']
        match = tester.get_match('I4580')
        self.assertEqual(match['ftdna'], "Marcus")

    def test_match_ancestors(self):
        tester = self.project['cassandra']
        ancestors = tester.get_ancestors('I4580')
        self.assertEqual(ancestors, 'F1614')        
