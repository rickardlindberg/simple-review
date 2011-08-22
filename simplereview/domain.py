from simplereview.json import json_list
from simplereview.json import json_object
from simplereview.json import json_value


class Review(object):

    def __init__(self, id_=None, name=None, date=None, diff=None, user=None):
        self.id_ = id_
        self.name = name
        self.date = date
        self.diff = diff
        self.user = user
        self.comments = []

    def add_comment(self, comment):
        self.comments.append(comment)

    def comments_json(self):
        return json_list(
            comment.to_json() for comment in self.comments
        )


class Comment(object):

    def __init__(self, review_id=None, date=None, user=None, text=None, line=None):
        self.review_id = review_id
        self.date = date
        self.user = user
        self.text = text
        self.line = line

    def to_json(self):
        return json_object({
            "date": json_value(str(self.date)),
            "user": json_value(self.user),
            "text": json_value(self.text),
            "line": json_value(self.line)
        })
