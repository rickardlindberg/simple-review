import web

from simplereview.diffparser import parse
from simplereview.json import json_list
from simplereview.json import json_object
from simplereview.json import json_value


class Review(object):

    def __init__(self, id_=None, title=None, date=None, diff=None,
                 diff_author=None, comments=None):
        self.id_ = id_
        self.title = title
        self.date = date
        self.diff = diff
        self.diff_author = diff_author
        self.comments = comments

    def parsed_diff(self):
        return parse(self.diff)

    def formatted_date(self):
        return format_date(self.date)


class Comment(object):

    def __init__(self, review_id=None, date=None, author=None, text=None,
                 line_number=None):
        self.review_id = review_id
        self.date = date
        self.author = author
        self.text = text
        self.line_number = line_number

    def is_line_comment(self):
        return self.line_number != -1

    def formatted_date(self):
        return format_date(self.date)

    def to_json(self):
        return json_object({
            "date": json_value(web.websafe(self.formatted_date())),
            "author": json_value(web.websafe(self.author)),
            "text": json_value(web.websafe(self.text)),
            "line_number": json_value(web.websafe(self.line_number))
        })


def format_date(date):
    return date.strftime("%d %b %Y")
