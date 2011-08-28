import unittest

from simplereview.domain import Comment


class TestComment(unittest.TestCase):

    def test_is_line_if_line_is_not_minus_1(self):
        self.assertTrue(Comment(line=1).is_line_comment())

    def test_is_not_line_if_line_is_minus_1(self):
        self.assertFalse(Comment(line=-1).is_line_comment())
