import datetime
import unittest

from simplereview.domain import Review
from simplereview.reviewlist import ReviewList


class ReviewListTest(unittest.TestCase):

    def test_has_section_for_today(self):
        self.given_today_is(2011, 8, 22)
        self.when_making_list_from([
            a_review_with_date(2011, 8, 22)
        ])
        self.assert_has_sections(["Today"])

    def test_has_section_for_yesterday(self):
        self.given_today_is(2010, 8, 23)
        self.when_making_list_from([
            a_review_with_date(2010, 8, 22)
        ])
        self.assert_has_sections(["Yesterday"])

    def test_has_section_for_this_week(self):
        self.given_today_is(2011, 8, 25)
        self.when_making_list_from([
            a_review_with_date(2011, 8, 22) # Monday
        ])
        self.assert_has_sections(["This Week"])

    def test_has_section_for_last_week(self):
        self.given_today_is(2011, 8, 25)
        self.when_making_list_from([
            a_review_with_date(2011, 8, 21) # Sunday
        ])
        self.assert_has_sections(["Last Week"])

    def test_has_section_for_earlier_than_last_week(self):
        self.given_today_is(2011, 8, 25)
        self.when_making_list_from([
            a_review_with_date(2011, 7, 21)
        ])
        self.assert_has_sections(["Older"])

    def test_has_multiple_sections(self):
        self.given_today_is(2011, 8, 23)
        self.when_making_list_from([
            a_review_with_date(2011, 8, 23),
            a_review_with_date(2011, 8, 22),
        ])
        self.assert_has_sections(["Today", "Yesterday"])

    def test_has_reviews_in_sections(self):
        self.given_today_is(2011, 8, 23)
        self.when_making_list_from([
            a_review_with_date(2011, 8, 23, name="review 1"),
            a_review_with_date(2011, 8, 23, name="review 2"),
        ])
        self.assert_has_reviews(["review 1", "review 2"])

    def given_today_is(self, year, month, day):
        self.now = datetime.datetime(year, month, day)

    def when_making_list_from(self, reviews):
        self.reviews = ReviewList(reviews, now_fn=lambda: self.now)

    def assert_has_sections(self, expected_section_names):
        self.assertEquals(len(expected_section_names), len(self.reviews.sections))
        self.assertEquals(
            "\n".join(expected_section_names),
            "\n".join(s.name for s in self.reviews.sections))

    def assert_has_reviews(self, expected_review_names):
        section = self.reviews.sections[0]
        self.assertEquals(len(expected_review_names), len(section.reviews))
        self.assertEquals(
            "\n".join(expected_review_names),
            "\n".join(s.name for s in section.reviews))


def a_review_with_date(year, month, day, name=""):
    return Review(date=datetime.datetime(year, month, day), name=name)
