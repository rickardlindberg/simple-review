function loadCommentsFor(review_id) {
    $.getJSON("/review/" + review_id + "/comments_json", function (commentsJson) {
        for (var line in commentsJson) {
            if (line !== "-1") {
                $("#line-margin-" + line + " .has-comment").show();

                var commentsDiv = $("<div/>").addClass("line-comments");
                $.each(commentsJson[line], function (i, comment) {
                    if (i !== 0) {
                        commentsDiv.append($("<hr/>"));
                    }
                    commentsDiv.append($("<div/>").addClass("line-comment").html(
                        "<i>by <b>" + comment.author + "</b> at " + comment.date + "</i><br />" +
                        comment.text
                    ));
                });
                $("#line-margin-" + line).append(commentsDiv);
            }
        }
    });
}

function registerMarginHoverHandlers() {
    $(".margin").hover(
        function () {
            $(this).find(".add-comment").show();

            var pos = $(this).find(".has-comment").offset();
            pos.top += 20;
            $(this).find(".line-comments").offset(pos);
            $(this).find(".line-comments").show();
        },
        function () {
            $(this).find(".add-comment").hide();

            $(this).find(".line-comments").hide();
        }
    );
}

function registerAddLineCommentClickHandlers() {
    $(".add-comment").click(
        function (event) {
            var id = $(this).parent().parent().attr("id");
            var line = id.substring(id.lastIndexOf("-") + 1);
            var pos = $(this).offset();
            pos.top += 20;
            pos.left += 20;
            $("#linenum").val(line);
            $("#line-comment-form").offset(pos);
            $("#line-comment-form").show();
            event.preventDefault();
        }
    );
}
