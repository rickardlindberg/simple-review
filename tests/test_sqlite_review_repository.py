import datetime
import os.path
import shutil
import tempfile
import unittest

from simplereview.domain import Review
from simplereview.repositories import SqliteReviewRepository


class SqliteReviewRepositoryTest(unittest.TestCase):

    def test_has_no_reviews_at_start(self):
        self.assertEquals(0, len(self.repo.list_by_date()))

    def test_has_one_review_after_adding_one(self):
        self.repo.save(Review())
        self.assertEquals(1, len(self.repo.list_by_date()))

    def test_returns_id_of_saved_review(self):
        id_ = self.repo.save(Review())
        self.assertNotEquals(None, id_)

    def test_saved_reviews_can_be_retrieved(self):
        self.repo.save(Review(title="fix bug", diff="diff...", diff_author="rick"))
        review = self.repo.list_by_date()[0]
        self.assertEquals("fix bug", review.title)
        self.assertEqual("diff...", review.diff)
        self.assertEqual("rick", review.diff_author)

    def test_adds_date_when_saving_review(self):
        self.repo.save(Review())
        review = self.repo.list_by_date()[0]
        self.assertTrue(isinstance(review.date, datetime.datetime))

    def test_adds_id_when_saving_review(self):
        self.repo.save(Review())
        review = self.repo.list_by_date()[0]
        self.assertNotEquals(None, review.id_)

    def test_gives_unique_ids_to_new_reviews(self):
        self.repo.save(Review())
        self.repo.save(Review())
        all_reviews = self.repo.list_by_date()
        self.assertNotEquals(all_reviews[0].id_, all_reviews[1].id_)

    def test_reviews_can_be_retrieved_by_id(self):
        id_ = self.repo.save(Review())
        review_by_list = self.repo.list_by_date()[0]
        review_by_id = self.repo.find_by_id(id_)
        self.assertEquals(review_by_list.title, review_by_id.title)

    def test_sorts_reviews_latest_first(self):
        self.repo.save(Review(title="first"))
        self.repo.save(Review(title="second"))
        self.assertEquals(
            ["second", "first"],
            [review.title for review in self.repo.list_by_date()])

    def test_can_add_comment_to_review(self):
        review_id = self.repo.save(Review())
        review = self.repo.find_by_id(review_id)
        self.repo.add_comment(review.id_, "rick", "comment")
        review = self.repo.find_by_id(review_id)
        self.assertEquals("rick", review.comments[0].author)
        self.assertEquals("comment", review.comments[0].text)

    def test_can_add_line_comment_to_review(self):
        review_id = self.repo.save(Review())
        review = self.repo.find_by_id(review_id)
        self.repo.add_comment(review.id_, "rick", "comment", 5)
        review = self.repo.find_by_id(review_id)
        self.assertEquals("rick", review.comments[0].author)
        self.assertEquals("comment", review.comments[0].text)
        self.assertEquals(5, review.comments[0].line_number)

    def test_adds_date_when_adding_comment(self):
        self.repo.save(Review())
        review = self.repo.list_by_date()[0]
        self.repo.add_comment(review.id_, "rick", "comment")
        comment = self.repo.list_by_date()[0].comments[0]
        self.assertTrue(isinstance(comment.date, datetime.datetime))

    def test_sorts_comment_latest_last(self):
        self.repo.save(Review())
        review = self.repo.list_by_date()[0]
        self.repo.add_comment(review.id_, "rick", "first")
        self.repo.add_comment(review.id_, "rick", "second")
        self.assertEquals(
            ["first", "second"],
            [comment.text for comment in self.repo.list_by_date()[0].comments])

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp("simplereview")
        db_path = os.path.join(self.tmp_dir, "db.sqlite")
        self.repo = SqliteReviewRepository(db_path)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
