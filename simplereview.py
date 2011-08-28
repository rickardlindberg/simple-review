#!/usr/bin/env python

import os
import os.path
import sys

ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, "libs"))

if os.getenv("SIMPLE_REVIEW_CONFIG", None) is None:
    os.environ["SIMPLE_REVIEW_CONFIG"] = "dev.config"

from simplereview.commentgrouper import CommentGrouper
from simplereview.domain import Review
from simplereview.reviewlist import ReviewList
import simplereview.config

import web

config = simplereview.config.read()

urls = (
    "/", "list_reviews",
    "/create_review", "create_review",
    "/review/(.*)/comments_json", "comments_json",
    "/review/(.*)/add_comment", "add_comment",
    "/review/(.*)", "review",
)

class list_reviews:
    def GET(self):
        return config.render.list_reviews(ReviewList(config.repo.list_by_date()))

class create_review:
    def POST(self):
        i = web.webapi.input()
        return "%s" % config.repo.save(Review(title=i.title, diff=i.diff, diff_author=i.diff_author))

class comments_json:
    def GET(self, review_id):
        web.header("Content-Type", "application/json")
        return CommentGrouper(config.repo.find_by_id(review_id).comments).to_json()

class add_comment:
    def POST(self, review_id):
        i = web.webapi.input()
        config.repo.add_comment(review_id, i.author, i.comment, i.line_number)
        web.seeother("/review/%s" % review_id)

class review:
    def GET(self, review_id):
        return config.render.review(config.repo.find_by_id(review_id))

if __name__ == "__main__":
    web.application(urls, globals()).run()
