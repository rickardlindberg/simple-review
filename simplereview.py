#!/usr/bin/env python

import os
import os.path
import sys

ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, "libs", "web.py-0.36"))

from simplereview.domain import Review
from simplereview.repositories import SqliteReviewRepository
from simplereview.reviewlist import ReviewList

import web

repo = SqliteReviewRepository(os.getenv("DB_PATH", "dev.db"))
render = web.template.render(os.getenv("TEMPLATE_DIR", "templates/"), base="base")
urls = (
    "/", "list_reviews",
    "/create_review", "create_review",
    "/review/(.*)/comments_json", "comments_json",
    "/review/(.*)/add_comment", "add_comment",
    "/review/(.*)", "review",
)

class list_reviews:
    def GET(self):
        return render.list_reviews(ReviewList(repo.list_by_date()))

class create_review:
    def POST(self):
        i = web.webapi.input()
        repo.save(Review(name=i.name, diff=i.diff, user=i.user))

class comments_json:
    def GET(self, review_id):
        web.header("Content-Type", "application/json")
        return repo.find_by_id(review_id).comments_json()

class add_comment:
    def POST(self, review_id):
        i = web.webapi.input()
        repo.add_comment(review_id, i.author, i.comment)
        web.seeother("/review/%s" % review_id)

class review:
    def GET(self, review_id):
        return render.review(repo.find_by_id(review_id))

if __name__ == "__main__":
    web.application(urls, globals()).run()
