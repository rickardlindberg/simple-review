import unittest

from simplereview.domain import Comment
from simplereview.domain import Review


class TestComment(unittest.TestCase):

    def test_is_line_if_line_is_not_minus_1(self):
        self.assertTrue(Comment(line_number=1).is_line_comment())

    def test_is_not_line_if_line_is_minus_1(self):
        self.assertFalse(Comment(line_number=-1).is_line_comment())


class ReviewTest(unittest.TestCase):

    def test_has_comments_returns_false_if_no_comments(self):
        self.assertFalse(Review(comments=[]).has_comments())

    def test_has_comments_returns_true_if_some_comment(self):
        self.assertTrue(Review(comments=[Comment()]).has_comments())
