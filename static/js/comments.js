function initComments(reviewId) {
    populateAuthorFiledInFormFromCookie();
    saveAuthorToCookieWhenSubmittingForm();
    showAddCommentImageWhenHoveringLine();
    showLineCommentsWhenHoveringCommentImage();
    showAddLineCommentFormWhenClickingAddCommentIcon();
    cloneForm();
    loadCommentsFor(reviewId);
}

function populateAuthorFiledInFormFromCookie() {
    $("input[name=author]").val($.cookie("commentAuthor"));
}

function saveAuthorToCookieWhenSubmittingForm() {
    $(".add-comment-form").submit(function () {
        var author = $(this).find("input[name=author]").val();
        $.cookie("commentAuthor", author, { expires: 100 });
    });
}

function showAddCommentImageWhenHoveringLine() {
    $(".line").hover(
        function () {
            $(this).find(".add-comment").show();
        },
        function () {
            $(this).find(".add-comment").hide();
        }
    );
}

function showLineCommentsWhenHoveringCommentImage() {
    $(".has-comment").hover(
        function () {
            var pos = $(this).position();
            var lineComments = $(this).parent().find(".line-comments");
            showElementAtAbsolutePosition(lineComments, pos.left, pos.top+20);
        },
        function () {
            $(this).parent().find(".line-comments").hide();
        }
    );
}

function showAddLineCommentFormWhenClickingAddCommentIcon() {
    $(".add-comment").click(
        function (event) {
            var id = $(this).attr("id");
            var line = id.substring(id.lastIndexOf("-") + 1);
            var pos = $(this).position();
            $("#line-comment-form").find("input[name=line_number]").val(line);
            showElementAtAbsolutePosition($("#line-comment-form"), pos.left+20, pos.top+20);
            event.preventDefault();
        }
    );
}

function showElementAtAbsolutePosition(element, left, top) {
    element.css("left", left);
    element.css("top", top);
    element.show();
}

function cloneForm() {
    $("#line-comment-form").append($(".add-comment-form").clone());
}

function loadCommentsFor(reviewId) {
    $.getJSON("/review/" + reviewId + "/comments_json", function (commentsJson) {
        for (var line in commentsJson) {
            var hasCommentImage = $(".line-number-" + line + " .has-comment");
            hasCommentImage.show();
            hasCommentImage.parent().append(createCommentsBox(commentsJson[line]));
        }
    });
}

function createCommentsBox(comments) {
    var commentsDiv = $("<div/>").addClass("line-comments");
    $.each(comments, function (i, comment) {
        if (i !== 0) {
            commentsDiv.append($("<hr/>"));
        }
        commentsDiv.append($("<div/>").addClass("line-comment").html(
            "<i>by <b>" + comment.author + "</b> at " + comment.date + "</i><br />" +
            comment.text
        ));
    });
    return commentsDiv;
}
