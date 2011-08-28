import os.path
import shutil
import subprocess
import tempfile
import time
import unittest
import urllib


class AcceptanceTest(unittest.TestCase):

    SITE_NAME = "test-site-name"

    def test_has_site_name_as_title(self):
        self.assert_page_contains("/", "<title>%s</title>" % self.SITE_NAME)

    def test_has_review_on_list_page(self):
        self.add_review_with_title("review 1")
        self.assert_page_contains("/", "review 1")

    def test_has_review_on_review_page(self):
        review_id = self.add_review_with_title("review 2")
        self.assert_page_contains("/review/%s" % review_id, "review 2")

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp("simplereview")
        self.config_path = os.path.join(self.tmp_dir, "test.config")
        self.db_path = os.path.join(self.tmp_dir, "test.db")
        self.start_server()
        self.wait_for_server_to_start()

    def start_server(self):
        self.write_config()
        os.putenv("SIMPLE_REVIEW_CONFIG", self.config_path)
        self.server_process = subprocess.Popen(
            ["python", "simplereview.py", "8081"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def write_config(self):
        f = open(self.config_path, "w")
        f.write("[site]\n")
        f.write("name = %s\n" % self.SITE_NAME)
        f.write("[db]\n")
        f.write("path = %s\n" % self.db_path)
        f.close()

    def wait_for_server_to_start(self):
        time.sleep(1)

    def add_review_with_title(self, title):
        request = urllib.urlopen("http://localhost:8081/create_review", urllib.urlencode({
            "title": title,
            "diff": "",
            "diff_author": ""
        }))
        return request.read().strip()

    def assert_page_contains(self, page, part):
        content = self.read_content_from(page)
        if part not in content:
            self.fail("Did not find '%s' in '%s'" % (part, content))
        
    def read_content_from(self, path):
        return urllib.urlopen("http://localhost:8081%s" % path).read()

    def tearDown(self):
        self.kill_server()
        shutil.rmtree(self.tmp_dir)

    def kill_server(self):
        self.server_process.kill()
