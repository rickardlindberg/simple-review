from simplereview.json import json_list
from simplereview.json import json_object


class CommentsGroupedByLineNumber(object):

    def __init__(self, comments):
        self.comments = {}
        self._group_comments(comments)

    def _group_comments(self, comments):
        for comment in comments:
            if comment.line_number != -1:
                self._add_comment(comment)

    def _add_comment(self, comment):
        if not self.comments.has_key(comment.line_number):
            self.comments[comment.line_number] = []
        self.comments[comment.line_number].append(comment)

    def get_lines(self):
        return self.comments.keys()

    def get_comments(self, line_number):
        return self.comments[line_number]

    def to_json(self):
        json_group = {}
        for key in self.comments:
            json_group[str(key)] = json_list(
                comment.to_json() for comment in self.comments[key]
            )
        return json_object(json_group)
