import unittest

from simplereview.diffparser import UnifiedDiffParser


class DiffParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = UnifiedDiffParser()

    def test_parses_all_files(self):
        diff = self.parser.parse("""
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
        """.strip())
        self.assertEquals(2, len(diff.files))
        self.assertEquals("a/.bashrc", diff.files[0].old)
        self.assertEquals("b/.bashrc", diff.files[0].new)
        self.assertEquals("a/.gitignore", diff.files[1].old)
        self.assertEquals("b/.gitignore", diff.files[1].new)

    def test_parses_chunks(self):
        diff = self.parser.parse("""
diff --git a/.vimrc b/.vimrc
index 3aabebf..549bdce 100644
--- a/.vimrc
+++ b/.vimrc
@@ -6,7 +6,6 @@ let g:snippets_dir="~/.vim/snippets"
 filetype plugin indent on
 
 " = Tab
-set tabstop=8
 set shiftwidth=4
 set softtabstop=4
 set expandtab
@@ -80,7 +79,6 @@ endfunction
 
 let mapleader = ","
 
-map <F2> :cn<CR>
 map <F7> :call GoToPrevEditedFile()<CR>
 map <F11> :set syntax=mail<CR>
 map <F12> :set spelllang=sv<CR>

        """.strip())
        self.assertEquals(2, len(diff.files[0].chunks))
        self.assertEquals(
            '@@ -6,7 +6,6 @@ let g:snippets_dir="~/.vim/snippets"',
            diff.files[0].chunks[0].line.content)
        self.assertEquals(
            '@@ -80,7 +79,6 @@ endfunction',
            diff.files[0].chunks[1].line.content)

    def test_parses_diff_lines_in_chunks(self):
        diff = self.parser.parse("""
diff --git a/.vimrc b/.vimrc
index 3aabebf..da2ded7 100644
--- a/.vimrc
+++ b/.vimrc
@@ -6,10 +6,10 @@ let g:snippets_dir="~/.vim/snippets"
 filetype plugin indent on
 
 " = Tab
-set tabstop=8
-set shiftwidth=4
+set tabstop=4
 set softtabstop=4
 set expandtab
+set shiftwidth=4
 
 " = Search
 set noignorecase

        """.strip())
        parts = diff.files[0].chunks[0].parts
        self.assertEquals(6, len(parts))
        self.assertEquals("context", parts[0].type_)
        self.assertEquals("removed", parts[1].type_)
        self.assertEquals("added", parts[2].type_)
        self.assertEquals("context", parts[3].type_)
        self.assertEquals("added", parts[4].type_)
        self.assertEquals("context", parts[5].type_)

    def test_parses_line_numbers(self):
        diff = self.parser.parse("""
diff --git a/.vimrc b/.vimrc
index 3aabebf..da2ded7 100644
--- a/.vimrc
+++ b/.vimrc
@@ -6,10 +6,10 @@ let g:snippets_dir="~/.vim/snippets"
 filetype plugin indent on
 
 " = Tab
-set tabstop=8
-set shiftwidth=4
+set tabstop=4
 set softtabstop=4
 set expandtab
+set shiftwidth=4
 
 " = Search
 set noignorecase

        """.strip())
        parts = diff.files[0].chunks[0].parts
        self.assertEquals(5, parts[0].lines[0].number)
        self.assertEquals(" filetype plugin indent on", parts[0].lines[0].content)
