import unittest

from simplereview.json import json_list
from simplereview.json import json_object
from simplereview.json import json_value


class JsonTest(unittest.TestCase):

    def test_escapes_quotes_in_string_values(self):
        self.assertEquals('"hell\\"o"', json_value('hell"o'))

    def test_escapes_backslash_in_string_values(self):
        self.assertEquals('"hell\\\\o"', json_value('hell\\o'))

    def test_escapes_forward_slash_in_string_values(self):
        self.assertEquals('"hell\\/o"', json_value('hell/o'))

    def test_escapes_backspace_in_string_values(self):
        self.assertEquals('"hell\\bo"', json_value('hell\bo'))

    def test_escapes_formfeed_in_string_values(self):
        self.assertEquals('"hell\\fo"', json_value('hell\fo'))

    def test_escapes_newline_in_string_values(self):
        self.assertEquals('"hell\\no"', json_value('hell\no'))

    def test_escapes_carriage_return_in_string_values(self):
        self.assertEquals('"hell\\ro"', json_value('hell\ro'))

    def test_escapes_tab_in_string_values(self):
        self.assertEquals('"hell\\to"', json_value('hell\to'))

    def test_escapes_all_correctly(self):
        self.assertEquals('"he\\"ll\\\\o"', json_value('he"ll\\o'))

    def test_converts_numbers(self):
        self.assertEquals('1', json_value(1))

    def test_can_do_lists(self):
        self.assertEquals('[1,hello]', json_list(["1", "hello"]))

    def test_can_do_object(self):
        self.assertEquals('{"a":1,"b":"hello"}', json_object({
            "a": "1",
            "b": "\"hello\""
        }))
