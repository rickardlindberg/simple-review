import datetime
import os
import sqlite3

from simplereview.domain import Review


class ReviewRepository(object):

    def save(self, review):
        raise NotImplementedError()

    def list_by_date(self):
        raise NotImplementedError()


class SqliteReviewRepository(ReviewRepository):

    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            self._create_db()

    def save(self, review):
        def insert(cursor):
            cursor.execute("insert into reviews (name, date) values (?, ?)", (review.name,
                datetime.datetime.now()))
        self._with_cursor(insert)

    def list_by_date(self):
        result = []
        def fn(cursor):
            cursor.execute("select * from reviews order by date desc")
            for review_row in cursor:
                result.append(Review(id_=review_row["id"], name=review_row["name"]))
        self._with_cursor(fn)
        return result

    def _create_db(self, cursor=None):
        if cursor:
            cursor.execute('''
                create table reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name text,
                    date date
                )
            ''')
        else:
            self._with_cursor(self._create_db)

    def _with_cursor(self, fn):
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        fn(cursor)
        connection.commit()
        cursor.close()
