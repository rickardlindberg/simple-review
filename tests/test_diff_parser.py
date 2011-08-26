import re
import unittest

from simplereview.diffparser import parse


class DiffParserTest(unittest.TestCase):

    def test_creates_one_file_per_file_in_diff(self):
        self.when_parsing("""
        diff --git a/.bashrc b/.bashrc
        index bef78b2..17e71d9 100644
        --- a/.bashrc
        +++ b/.bashrc
        @@ -9,4 +9,3 @@ fi
         . ~/.bashrc_files/aliases.sh
         . ~/.bashrc_files/hg.sh
         . ~/.bashrc_files/diff.sh
        -. ~/.bashrc_files/prompt.sh
        diff --git a/.gitignore b/.gitignore
        index bf7dec6..f0e98ac 100644
        --- a/.gitignore
        +++ b/.gitignore
        @@ -1,4 +1,3 @@
         local.vim
         local.sh
         .netrwhist
        -.vim/spell
        """)
        self.assert_diff_has_files((
            ("a/.bashrc", "b/.bashrc"),
            ("a/.gitignore", "b/.gitignore"),
        ))

    def test_parses_all_lines_for_a_file(self):
        self.when_parsing("""
        diff --git a/.bashrc b/.bashrc
        index bef78b2..17e71d9 100644
        --- a/.bashrc
        +++ b/.bashrc
        @@ -9,4 +9,3 @@ fi
         . ~/.bashrc_files/aliases.sh
         . ~/.bashrc_files/hg.sh
         . ~/.bashrc_files/diff.sh
        -. ~/.bashrc_files/prompt.sh
        """)
        self.assertEquals(5, len(self.diff.files[0].lines))

    def test_includes_type_for_hunk_lines(self):
        self.when_parsing("""
        diff --git a/.bashrc b/.bashrc
        index bef78b2..17e71d9 100644
        --- a/.bashrc
        +++ b/.bashrc
        @@ -9,4 +9,3 @@ fi
         . ~/.bashrc_files/aliases.sh
         . ~/.bashrc_files/hg.sh
         . ~/.bashrc_files/diff.sh
        -. ~/.bashrc_files/prompt.sh
        """)
        self.assertEquals("hunk", self.diff.files[0].lines[0].type_)

    def test_includes_type_for_context_lines(self):
        self.when_parsing("""
        diff --git a/.bashrc b/.bashrc
        index bef78b2..17e71d9 100644
        --- a/.bashrc
        +++ b/.bashrc
        @@ -9,4 +9,3 @@ fi
         . ~/.bashrc_files/aliases.sh
         . ~/.bashrc_files/hg.sh
         . ~/.bashrc_files/diff.sh
        -. ~/.bashrc_files/prompt.sh
        """)
        self.assertEquals("context", self.diff.files[0].lines[1].type_)

    def test_treat_empty_lines_as_context_lines(self):
        self.when_parsing("""
        diff --git a/.bashrc b/.bashrc
        index bef78b2..17e71d9 100644
        --- a/.bashrc
        +++ b/.bashrc
        @@ -9,4 +9,3 @@ fi

         . ~/.bashrc_files/hg.sh
         . ~/.bashrc_files/diff.sh
        -. ~/.bashrc_files/prompt.sh
        """)
        self.assertEquals("context", self.diff.files[0].lines[1].type_)

    def test_includes_type_for_removed_lines(self):
        self.when_parsing("""
        diff --git a/.bashrc b/.bashrc
        index bef78b2..17e71d9 100644
        --- a/.bashrc
        +++ b/.bashrc
        @@ -9,4 +9,3 @@ fi
         . ~/.bashrc_files/aliases.sh
         . ~/.bashrc_files/hg.sh
         . ~/.bashrc_files/diff.sh
        -. ~/.bashrc_files/prompt.sh
        """)
        self.assertEquals("removed", self.diff.files[0].lines[4].type_)

    def test_includes_type_for_added_lines(self):
        self.when_parsing("""
        diff --git a/.bashrc b/.bashrc
        index bef78b2..17e71d9 100644
        --- a/.bashrc
        +++ b/.bashrc
        @@ -9,4 +9,3 @@ fi
         . ~/.bashrc_files/aliases.sh
         . ~/.bashrc_files/hg.sh
         . ~/.bashrc_files/diff.sh
        +. ~/.bashrc_files/prompt.sh
        """)
        self.assertEquals("added", self.diff.files[0].lines[4].type_)

    def test_parses_no_newline_line_as_context(self):
        self.when_parsing("""
        diff --git a/.bashrc b/.bashrc
        index bef78b2..17e71d9 100644
        --- a/.bashrc
        +++ b/.bashrc
        @@ -9,4 +9,3 @@ fi
         . ~/.bashrc_files/aliases.sh
         . ~/.bashrc_files/hg.sh
         . ~/.bashrc_files/diff.sh
        -. ~/.bashrc_files/prompt.sh
        \\ No newline at end of file
        """)
        self.assertEquals("context", self.diff.files[0].lines[5].type_)

    def test_includes_original_line_number_for_lines(self):
        self.when_parsing("""
        diff --git a/.bashrc b/.bashrc
        index bef78b2..17e71d9 100644
        --- a/.bashrc
        +++ b/.bashrc
        @@ -9,4 +9,3 @@ fi
         . ~/.bashrc_files/aliases.sh
         . ~/.bashrc_files/hg.sh
         . ~/.bashrc_files/diff.sh
        -. ~/.bashrc_files/prompt.sh
        """)
        self.assertEquals(5, self.diff.files[0].lines[0].number)

    def when_parsing(self, indented_diff_text):
        indent_expression = re.compile(r"^        ", flags=re.MULTILINE)
        diff_text = indent_expression.sub("", indented_diff_text.strip())
        self.diff = parse(diff_text)

    def assert_diff_has_files(self, files):
        self.assertEquals(len(files), len(self.diff.files))
        for i in range(len(files)):
            self.assertEquals(files[i][0], self.diff.files[i].old)
            self.assertEquals(files[i][1], self.diff.files[i].new)
