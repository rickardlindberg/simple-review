from simplereview.json import json_list
from simplereview.json import json_object
from simplereview.json import json_value


def parse(diff_text):
    return DiffParser().parse(diff_text)


class DiffParser(object):

    def parse(self, diff_text):
        self.reader = LineReader(diff_text)
        return Diff(self._parse_files())

    def _parse_files(self):
        files = []
        while self.reader.has_line():
            self._skip_to_file()
            files.append(self._read_file())
        return files

    def _skip_to_file(self):
        while not self.reader.peek().startswith("---"):
            self.reader.pop_line()

    def _read_file(self):
        old = self._parse_file_name()
        new = self._parse_file_name()
        lines = self._parse_lines()
        return File(old, new, lines)

    def _parse_file_name(self):
        return self.reader.pop_line()[1][4:]

    def _parse_lines(self):
        lines = []
        while self.reader.has_line() and self.reader.peek()[0] in "+-@ \\":
            (number, content) = self.reader.pop_line()
            line = Line(number, content, self._get_line_type(content))
            lines.append(line)
        return lines

    def _get_line_type(self, content):
        return {
            "@": "hunk",
            " ": "context",
            "+": "added",
            "-": "removed",
            "\\": "context",
        }.get(content[0], "")


class LineReader(object):

    def __init__(self, text):
        self._split_lines(text)

    def _split_lines(self, text):
        self.lines = text.split("\n")
        for i in range(len(self.lines)):
            self.lines[i] = (i+1, self.lines[i])

    def peek(self):
        return self.lines[0][1]

    def pop_line(self):
        return self.lines.pop(0)

    def has_line(self):
        return len(self.lines) > 0


class Diff(object):

    def __init__(self, files):
        self.files = files

    def to_json(self):
        return json_list(
            f.to_json() for f in self.files
        )


class File(object):

    def __init__(self, old, new, lines):
        self.old = old
        self.new = new
        self.lines = lines

    def to_json(self):
        return json_object({
            "old": json_value(self.old),
            "new": json_value(self.new),
            "lines": json_list(
                l.to_json() for l in self.lines
            ),
        })


class Line(object):

    def __init__(self, number, content, type_):
        self.number = number
        self.content = content
        self.type_ = type_

    def to_json(self):
        return json_object({
            "number": json_value(self.number),
            "content": json_value(self.content),
            "type": json_value(self.type_),
        })