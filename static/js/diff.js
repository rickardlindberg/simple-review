var CommentLoader = {

    load: function (review_id) {
        $.getJSON("/review/" + review_id + "/comments_json", function (commentsJson) {
            for (var line in commentsJson) {
                if (line !== "-1") {
                    $("#line-margin-" + line + " .has-comment").show();

                    var commentsDiv = $("<div/>").addClass("line-comments");
                    $.each(commentsJson[line], function (i, comment) {
                        commentsDiv.append($("<div/>").addClass("line-comment").html(
                            "by <b>" + comment.user + "</b> at " + comment.date +
                            comment.text
                        ));
                    });
                    $("#line-margin-" + line).append(commentsDiv);
                }
            }
        });
    }

};
