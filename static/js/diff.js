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
