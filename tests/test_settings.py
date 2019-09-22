import os
import unittest

from gensplorer.services.settings import Settings
from gensplorer import services


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.settings = Settings("testfile.json")

    def tearDown(self):
        os.unlink("testfile.json")

    def test_set_and_get(self):
        self.settings.set("somekey", 5)
        self.assertDictEqual({'somekey': 5}, self.settings.settings)
        v = self.settings.get("somekey")

        self.assertEqual(v, 5)

    def test_set_and_get_with_parents(self):
        key = "foo.bar"
        value = 5

        self.settings.set(key, value)
        self.assertDictEqual({'foo': {'bar': 5}}, self.settings.settings)
        v = self.settings.get(key)
        self.assertEqual(value, v)

    def test_set_and_get_with_multiple_parents(self):
        key = "foo.bar.baz"
        value = 5

        self.settings.set(key, value)
        self.assertDictEqual({'foo': {'bar': {'baz': 5}}},
                             self.settings.settings)
        v = self.settings.get(key)
        self.assertEqual(value, v, self.settings.settings)

    def test_file_created(self):
        self.assertTrue(os.path.isfile("testfile.json"))

    def test_settings_to_string(self):
        self.settings.set('foo', 'bar')
        self.assertEqual(str(self.settings), '{\n    "foo": "bar"\n}')

    def test_global_set_and_get(self):
        services.set("testsetting", 9)
        v = services.get("testsetting")
        self.assertEqual(9, v)
