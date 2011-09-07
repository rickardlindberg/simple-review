def line_anchor(line_number):
    try:
        line_number = int(line_number)
    except ValueError:
        return ""
    if line_number == -1:
        return ""
    else:
        return "#%s" % line_number
