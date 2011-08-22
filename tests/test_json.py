import unittest

import simplereview.json


class JsonTest(unittest.TestCase):

    def test_escapes_quotes_in_string_values(self):
        self.assertEquals('"\\"hello\\""', simplereview.json.json_value('"hello"'))

    def test_escapes_backslash_in_string_values(self):
        self.assertEquals('"hell\\\\o"', simplereview.json.json_value('hell\\o'))

    def test_escapes_all_correctly(self):
        self.assertEquals('"he\\"ll\\\\o"', simplereview.json.json_value('he"ll\\o'))

    def test_converts_numbers(self):
        self.assertEquals('1', simplereview.json.json_value(1))

    def test_can_do_lists(self):
        self.assertEquals('[1,hello]', simplereview.json.json_list(["1", "hello"]))

    def test_can_do_object(self):
        self.assertEquals('{"a":1,"b":"hello"}', simplereview.json.json_object({
            "a": "1",
            "b": "\"hello\""
        }))
