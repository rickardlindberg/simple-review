import unittest

from simplereview.lineanchor import line_anchor


class LineAnchorTest(unittest.TestCase):

    def test_returns_empty_string_if_miuns_one(self):
        self.assertEquals("", line_anchor(-1))

    def test_returns_empty_string_if_not_number(self):
        self.assertEquals("", line_anchor("hello"))

    def test_returns_anchor_string_for_numbers(self):
        self.assertEquals("#33", line_anchor(33))

    def test_returns_anchor_string_for_numbers_given_as_strings(self):
        self.assertEquals("#22", line_anchor("22"))
