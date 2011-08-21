import os

from simplereview.domain import Review
from simplereview.repositories import SqliteReviewRepository

import web

DB_PATH = os.getenv("DB_PATH", "dev.db")
TEMPLATE_DIR = os.getenv("TEMPLATE_DIR", "templates/")
URLS = (
    "/", "list_reviews",
    "/create_review", "create_review",
    "/review/(.*)", "review",
)

render = web.template.render(TEMPLATE_DIR, base="base")
repo = SqliteReviewRepository(DB_PATH)

class list_reviews:
    def GET(self):
        return render.list_reviews(repo.list_by_date())

class review:
    def GET(self, id_):
        r = None
        for review in repo.list_by_date():
            if str(review.id_) == str(id_):
                r = review
        return render.review(r)

class create_review:
    def POST(self):
        i = web.webapi.input()
        repo.save(Review(name=i.name))

if __name__ == "__main__":
    web.application(URLS, globals()).run()
