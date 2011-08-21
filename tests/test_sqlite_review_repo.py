import shutil
import tempfile
import unittest
import os.path

from simplereview.domain import Review
from simplereview.repositories import SqliteReviewRepository


class SqliteReviewRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp("simplereview")
        db_path = os.path.join(self.tmp_dir, "db.sqlite")
        self.repo = SqliteReviewRepository(db_path)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_saved_reviews_can_be_retrieved(self):
        self.repo.save(self.a_review_with_name("fix bug"))
        reviews = self.repo.list_by_date()
        self.assert_contains_one_review_with_name(reviews, "fix bug")

    def test_adds_id_to_saved_review(self):
        self.repo.save(self.a_review_with_name("foo"))
        reviews = self.repo.list_by_date()
        self.assertNotEquals(None, reviews[0].id_)

    def test_two_added_have_different_ids(self):
        self.repo.save(self.a_review_with_name("foo"))
        self.repo.save(self.a_review_with_name("bar"))
        reviews = self.repo.list_by_date()
        self.assertNotEquals(reviews[0].id_, reviews[1].id_)

    def test_reviews_are_retrieved_in_correct_order(self):
        self.repo.save(self.a_review_with_name("first"))
        self.repo.save(self.a_review_with_name("second"))
        reviews = self.repo.list_by_date()
        self.assertEquals(
            ["second", "first"],
            [review.name for review in reviews])

    def a_review_with_name(self, name):
        return Review(name=name)

    def assert_contains_one_review_with_name(self, reviews, name):
        self.assertEquals(1, len(reviews))
        self.assertEquals(name, reviews[0].name)
