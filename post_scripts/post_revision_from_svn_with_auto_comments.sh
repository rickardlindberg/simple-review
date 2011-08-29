#!/bin/sh

SVN_SERVER=""
REVIEW_SERVER="http://localhost:8080"
DIFF_FILE_NAME="tmp.diff"

post_revision() {
    extract_review_data
    review_id=$(post_review)
    post_comments
    rm ${DIFF_FILE_NAME}
}

extract_review_data() {
    svn diff -c${revision} ${SVN_SERVER} > $DIFF_FILE_NAME
    message=$(svn log -r${revision} ${SVN_SERVER} 2>&1 | head -n4 | tail -n1)
    author=$(svn log -r${revision} ${SVN_SERVER} 2>&1 | head -n2 | tail -n1 | awk '{ print $3 }')
}

post_review() {
    curl \
        --silent \
        --data-urlencode "title=r${revision}: ${message}" \
        --data-urlencode "diff_author=${author}" \
        --data-urlencode "diff@${DIFF_FILE_NAME}" \
        ${REVIEW_SERVER}/create_review
}

post_comments() {
    comment_on_added_pattern "if" "no if statements allowed"
    comment_on_added_pattern "for" "use while instead of for"
}

comment_on_added_pattern() {
    for line_number in $(look_for_added_pattern "$1"); do
        post_comment "$2" > /dev/null
    done
}

look_for_added_pattern() {
    grep -n "^+ .*$1" ${DIFF_FILE_NAME} | tr ':' ' ' | awk '{ print $1 }'
}

post_comment() {
    curl \
        --silent \
        --data-urlencode "author=review-bot" \
        --data-urlencode "comment=${1}" \
        --data-urlencode "line_number=${line_number}" \
        ${REVIEW_SERVER}/review/${review_id}/add_comment
}

usage() {
    echo "Usage: $0 revision"
}

if [ -n "$1" ]; then
    revision="$1"
    post_revision
else
    usage
fi
