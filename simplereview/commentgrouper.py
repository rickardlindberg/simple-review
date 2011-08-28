from simplereview.json import json_list
from simplereview.json import json_object


class CommentGrouper(object):

    def __init__(self, comments):
        self.group = {}
        for comment in comments:
            if not self.group.has_key(comment.line_number):
                self.group[comment.line_number] = []
            self.group[comment.line_number].append(comment)
        self.keys = self.group.keys()

    def get(self, line_number):
        return self.group[line_number]

    def to_json(self):
        json_group = {}
        for key in self.group:
            json_group[str(key)] = json_list(
                comment.to_json() for comment in self.group[key]
            )
        return json_object(json_group)
