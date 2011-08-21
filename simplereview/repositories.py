import datetime
import os
import sqlite3

from simplereview.domain import Comment
from simplereview.domain import Review


class ReviewRepository(object):

    def save(self, review):
        raise NotImplementedError()

    def list_by_date(self):
        raise NotImplementedError()

    def find_by_id(self, id_):
        raise NotImplementedError()

    def add_comment(self, id_, user, text, line=-1):
        raise NotImplementedError()


class SqliteReviewRepository(ReviewRepository):

    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            self._create_db()

    def save(self, review):
        def insert(cursor):
            cursor.execute("insert into reviews (name, date, diff, user) values (?, ?, ?, ?)", (
                review.name,
                datetime.datetime.now(),
                review.diff,
                review.user
            ))
        self._with_cursor(insert)

    def list_by_date(self):
        result = []
        def fn(cursor):
            cursor.execute("select * from reviews order by date desc")
            for row in cursor:
                result.append(self._row_to_review(row))
        self._with_cursor(fn)
        return result

    def find_by_id(self, id_):
        def fn(cursor):
            cursor.execute("select * from reviews where id=?", str(id_))
            return self._row_to_review(cursor.fetchone())
        return self._with_cursor(fn)

    def add_comment(self, id_, user, text, line=-1):
        def insert(cursor):
            cursor.execute("insert into comments (review_id, date, user, text, line) values (?, ?, ?, ?, ?)", (
                id_,
                datetime.datetime.now(),
                user,
                text,
                line
            ))
        self._with_cursor(insert)

    def _row_to_review(self, row):
        review = Review(
            id_=row["id"],
            name=row["name"],
            date=row["date"],
            diff=row["diff"],
            user=row["user"]
        )
        self._add_comments(review)
        return review

    def _add_comments(self, review):
        def fn(cursor):
            cursor.execute("select * from comments where review_id=? order by date desc", str(review.id_))
            for row in cursor:
                review.add_comment(self._row_to_comment(row))
        self._with_cursor(fn)

    def _row_to_comment(self, row):
        return Comment(
            review_id=row["review_id"],
            date=row["date"],
            user=row["user"],
            text=row["text"],
            line=row["line"]
        )

    def _create_db(self, cursor=None):
        if cursor:
            cursor.execute('''
                create table reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name text,
                    date date,
                    diff text,
                    user text
                )
            ''')
            cursor.execute('''
                create table comments (
                    review_id integer,
                    date date,
                    user text,
                    text text,
                    line text
                )
            ''')
        else:
            self._with_cursor(self._create_db)

    def _with_cursor(self, fn):
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        return_value = fn(cursor)
        connection.commit()
        cursor.close()
        return return_value
