import unittest

from simplereview.commentgrouper import CommentGrouper
from simplereview.domain import Comment


class CommentGrouperTest(unittest.TestCase):

    def test_groups_by_line_number(self):
        group = CommentGrouper([
            Comment(line_number=-1),
            Comment(line_number=4),
        ])
        self.assertEquals(2, len(group.keys))

    def test_can_retrieve_comments_in_group(self):
        group = CommentGrouper([
            Comment(line_number=-1),
            Comment(line_number=4),
            Comment(line_number=4),
        ])
        self.assertEquals(1, len(group.get(-1)))
        self.assertEquals(2, len(group.get(4)))
