#!/usr/bin/env python

import os
import os.path

from simplereview.domain import Review
from simplereview.repositories import SqliteReviewRepository

DB_PATH = "db.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

repo = SqliteReviewRepository(DB_PATH)
repo.save(Review(name="test review"))
