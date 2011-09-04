import unittest

from simplereview.commentgrouper import CommentsGroupedByLineNumber
from simplereview.domain import Comment


class CommentsGroupedByLineNumberTest(unittest.TestCase):

    def test_groups_comments_by_line_number(self):
        group = CommentsGroupedByLineNumber([
            Comment(line_number=1),
            Comment(line_number=4),
        ])
        self.assertEquals(2, len(group.get_lines()))

    def test_can_retrieve_comments_in_group(self):
        group = CommentsGroupedByLineNumber([
            Comment(line_number=1),
            Comment(line_number=4),
            Comment(line_number=4),
        ])
        self.assertEquals(1, len(group.get_comments(1)))
        self.assertEquals(2, len(group.get_comments(4)))

    def test_can_excludes_invalid_line_numbers(self):
        group = CommentsGroupedByLineNumber([
            Comment(line_number=-1),
            Comment(line_number=4),
        ])
        self.assertEquals(1, len(group.get_lines()))
