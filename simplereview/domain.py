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


class Comment(object):

    def __init__(self, review_id=None, date=None, user=None, text=None, line=None):
        self.review_id = review_id
        self.date = date
        self.user = user
        self.text = text
        self.line = line
