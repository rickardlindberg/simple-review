var DiffLoader = {

    load: function (review_id, containerElement) {
        $.getJSON("/review_diff/" + review_id, function (diffJson) {
            DiffDomBuilder.build(diffJson).appendTo(containerElement);
            CommentLoader.load(review_id);
        });
    }

};

var CommentLoader = {

    load: function (review_id) {
        $.getJSON("/review/" + review_id + "/comments_json", function (commentsJson) {
            $.each(commentsJson, function (i, comment) {
                if (comment.line !== "-1") {
                    $("#line-margin-" + comment.line).show();
                }
            });
        });
    }

};

var DiffDomBuilder = {

    build: function (diffJson) {
        var diffDiv = $("<div/>").addClass("diff");
        DiffDomBuilder._buildFiles(diffDiv, diffJson);
        return diffDiv;
    },

    _buildFiles: function (diffDiv, diffedFiles) {
        $.each(diffedFiles, function (i, diffedFile) {
            var fileDiv = $("<div/>").addClass("file");
            fileDiv.append($("<div/>").addClass("file-header").text(diffedFile.old));
            DiffDomBuilder._buildLines(fileDiv, diffedFile);
            diffDiv.append(fileDiv);
        });
    },

    _buildLines: function (fileDiv, diffedFile) {
        $.each(diffedFile.lines, function (i, line) {
            DiffDomBuilder._buildLine(line).appendTo(fileDiv);
        });
    },

    _buildLine: function (jsonLine) {
        return $("<div/>").addClass("line-" + jsonLine.type).append(
            $("<div/>").addClass("margin").append(
                $("<div id=\"line-margin-"+jsonLine.number+"\"/>").addClass("margin-content").html('<img src="/static/images/comment.png" border="0" />').hide()),
            $("<pre/>").text(jsonLine.content));
    }

};
