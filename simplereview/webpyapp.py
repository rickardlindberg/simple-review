import os

from simplereview.diffparser import UnifiedDiffParser
from simplereview.domain import Review
from simplereview.repositories import SqliteReviewRepository

import web

DB_PATH = os.getenv("DB_PATH", "dev.db")
TEMPLATE_DIR = os.getenv("TEMPLATE_DIR", "templates/")
URLS = (
    "/", "list_reviews",
    "/create_review", "create_review",
    "/review/(.*)/comments_json", "comments_json",
    "/review/(.*)/add_comment", "add_comment",
    "/review/(.*)", "review",
    "/review_diff/(.*)", "review_diff",
)

render = web.template.render(TEMPLATE_DIR, base="base")
repo = SqliteReviewRepository(DB_PATH)
diff_parser = UnifiedDiffParser()

class list_reviews:
    def GET(self):
        return render.list_reviews(repo.list_by_date())

class review:
    def GET(self, id_):
        return render.review(repo.find_by_id(id_))

class review_diff:
    def GET(self, id_):
        web.header("Content-Type", "application/json")
        return diff_parser.parse(repo.find_by_id(id_).diff).to_json()

class comments_json:
    def GET(self, id_):
        web.header("Content-Type", "application/json")
        return repo.find_by_id(id_).comments_json()

class add_comment:
    def POST(self, review_id):
        i = web.webapi.input()
        repo.add_comment(review_id, i.author, i.comment)
        web.seeother("/review/%s" % review_id)

class create_review:
    def POST(self):
        i = web.webapi.input()
        repo.save(Review(name=i.name))

if __name__ == "__main__":
    web.application(URLS, globals()).run()
