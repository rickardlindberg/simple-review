function diff(element, id) {
    new Ajax.Request('/review_diff/' + id, {
        method: "get",
        onSuccess: function (transport) {
            var response = transport.responseText || "{}";
            var json = response.evalJSON();
            output(element, json);
        },
        onFailure: function () {
            alert('Something went wrong...')
        }
    });
}

function output(element, json) {
    json.each(function (file) {
        element.appendChild(file_to_html(file));
    });
}

function file_to_html(file) {
    var file_div = div("file");

    header = div("file-header");
    header.appendChild(span(file.old));
    file_div.appendChild(header);

    file.hunks.each(function (hunk) {
        hunk_to_html(file_div, hunk);
    });
    return file_div;
}

function hunk_to_html(file_div, hunk) {
    file_div.appendChild(line_to_html(hunk.line, "hunk"));
    hunk.parts.each(function (part) {
        part.lines.each(function (line) {
            file_div.appendChild(line_to_html(line, part.type));
        });
    });
}

function line_to_html(line, type) {
    var line_div = div("line");
    var margin_div = div("margin");
    var content_div = div("content");

    margin_div.appendChild(span(line.number));

    Element.addClassName(content_div, type);
    content_div.appendChild(span(line.content));

    line_div.appendChild(margin_div);
    line_div.appendChild(content_div);
    return line_div;
}

function span(text) {
    var span = document.createElement("pre");
    span.innerHTML = text;
    return span;
}

function div(className) {
    var div = document.createElement("div");
    Element.addClassName(div, className);
    return div;
}
