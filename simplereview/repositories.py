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

    def add_comment(self, review_id, user, text, line=-1):
        raise NotImplementedError()


class SqliteReviewRepository(ReviewRepository):

    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            self._create_db()

    def save(self, review):
        def execure_insert_query(cursor):
            cursor.execute("insert into reviews (name, date, diff, user) values (?, ?, ?, ?)", (
                review.name,
                datetime.datetime.now(),
                review.diff,
                review.user
            ))
            return cursor.lastrowid
        return self._with_cursor(execure_insert_query)

    def list_by_date(self):
        result = []
        def execute_select_query(cursor):
            cursor.execute("select * from reviews order by date desc")
            for row in cursor:
                result.append(self._row_to_review(row))
        self._with_cursor(execute_select_query)
        return result

    def find_by_id(self, id_):
        def execute_select_query(cursor):
            cursor.execute("select * from reviews where id=?", (str(id_),))
            return self._row_to_review(cursor.fetchone())
        return self._with_cursor(execute_select_query)

    def add_comment(self, review_id, user, text, line=-1):
        def execute_insert_query(cursor):
            cursor.execute("insert into comments (review_id, date, user, text, line) values (?, ?, ?, ?, ?)", (
                review_id,
                datetime.datetime.now(),
                user,
                text,
                line
            ))
        self._with_cursor(execute_insert_query)

    def _row_to_review(self, row):
        review = Review(
            id_=row["id"],
            name=row["name"],
            date=row["date"],
            diff=row["diff"],
            user=row["user"],
            comments=self._fetch_comments(row["id"]),
        )
        return review

    def _fetch_comments(self, review_id):
        def execute_select_query(cursor):
            comments = []
            cursor.execute("select * from comments where review_id=? order by date asc", (str(review_id),))
            for row in cursor:
                comments.append(self._row_to_comment(row))
            return comments
        return self._with_cursor(execute_select_query)

    def _row_to_comment(self, row):
        return Comment(
            review_id=row["review_id"],
            date=row["date"],
            user=row["user"],
            text=row["text"],
            line=row["line"]
        )

    def _create_db(self):
        def execute_create_queries(cursor):
            cursor.execute("""
            create table reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name text,
                date timestamp,
                diff text,
                user text
            )
            """)
            cursor.execute("""
            create table comments (
                review_id integer,
                date timestamp,
                user text,
                text text,
                line integer
            )
            """)
        self._with_cursor(execute_create_queries)

    def _with_cursor(self, fn):
        connection = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        return_value = fn(cursor)
        connection.commit()
        cursor.close()
        return return_value
