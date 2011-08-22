def json_value(python_value):
    if isinstance(python_value, int):
        return str(python_value)
    else:
        return '"%s"' % _string_escape(python_value)

def _string_escape(string):
    return string.replace("\\", "\\\\").replace('"', '\\"')

def json_list(json_values):
    return "[" + ",".join(json_values) + "]"

def json_object(json_values):
    pairs = []
    for key in json_values:
        pairs.append('"%s":%s' % (key, json_values[key]))
    return "{" + ",".join(pairs) + "}"
