from ConfigParser import ConfigParser
import os
import os.path

import web

from simplereview.repositories import SqliteReviewRepository


def read():
    path = os.getenv("SIMPLE_REVIEW_CONFIG", None)
    if path is None:
        raise Exception("Environment variable SIMPLE_REVIEW_CONFIG not defined.")
    if not os.path.exists(path):
        raise Exception("Could not find configuration file '%s'" % path)
    parser = ConfigParser()
    parser.read(path)
    return Config(
        site_name=parser.get("site", "name"),
        repo=SqliteReviewRepository(parser.get("db", "path")))


class Config(object):

    def __init__(self, site_name, repo):
        self.site_name = site_name
        self.repo = repo
        self.render = web.template.render("templates/", base="base", globals={
            "site_name": self.site_name
        })
