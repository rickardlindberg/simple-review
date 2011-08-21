import os.path
import shutil
import subprocess
import tempfile
import time
import unittest
import urllib


class AcceptanceTest(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp("simplereview")
        self.start_server()
        self.wait_for_server_to_start()

    def tearDown(self):
        self.kill_server()
        shutil.rmtree(self.tmp_dir)

    def start_server(self):
        os.putenv("DB_PATH", os.path.join(self.tmp_dir, "foo.db"))
        self.server_process = subprocess.Popen(["python", "simplereview/webpyapp.py"])

    def wait_for_server_to_start(self):
        time.sleep(1)

    def kill_server(self):
        self.server_process.kill()

    def test_has_review_on_list_page(self):
        self.add_review_with_name("review 1")
        self.assert_page_contains("/", "review 1")

    def test_has_review_on_review_page(self):
        self.add_review_with_name("review 2")
        self.assert_page_contains("/review/1", "review 2")

    def add_review_with_name(self, name):
        params = urllib.urlencode({
            "name": name
        })
        urllib.urlopen("http://localhost:8080/create_review", params)

    def assert_page_contains(self, page, part):
        content = self.read_content_from(page)
        if part not in content:
            self.fail("Did not find '%s' in '%s'" % (part, content))
        
    def read_content_from(self, path):
        return urllib.urlopen("http://localhost:8080%s" % path).read()
