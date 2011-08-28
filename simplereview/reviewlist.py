import datetime


class ReviewList(object):

    def __init__(self, reviews, now_fn=datetime.datetime.now):
        self.today = now_fn().date()
        self.sections = []
        sections = (
            ("Today", self._is_today),
            ("Yesterday", self._was_yeasterday),
            ("This week", self._was_this_week),
            ("Last week", self._was_last_week),
            ("Older", lambda review: True),
        )
        for (title, criteria) in sections:
            l = []
            while len(reviews) > 0 and criteria(reviews[0]):
                l.append(reviews.pop(0))
            if l:
                self.sections.append(Section(title, l))

    def _is_today(self, review):
        return review.date.date() == self.today

    def _was_yeasterday(self, review):
        return review.date.date() == self.today - datetime.timedelta(days=1)

    def _was_this_week(self, review):
        return review.date.date() in self._this_weeks_dates()

    def _was_last_week(self, review):
        return review.date.date() in self._last_weeks_dates()

    def _last_weeks_dates(self):
        one_week = datetime.timedelta(7)
        return [date - one_week for date in self._this_weeks_dates()]

    def _this_weeks_dates(self):
        dates = []
        monday = self._find_monday()
        for i in range(7):
            dates.append(monday + datetime.timedelta(days=i))
        return dates

    def _find_monday(self):
        MONDAY = 0
        day = self.today
        while day.weekday() != MONDAY:
            day = day - datetime.timedelta(days=1)
        return day


class Section(object):

    def __init__(self, title, reviews):
        self.title = title
        self.reviews = reviews
