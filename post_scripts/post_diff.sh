#!/bin/sh

post_review() {
    curl \
        --data-urlencode "title=${title}" \
        --data-urlencode "diff_author=${diff_author}" \
        --data-urlencode "diff@${DIFF_FILE_NAME}" \
        ${SERVER}/create_review
}

SERVER="http://localhost:8080"
title="$(basename $1)"
diff_author="diff-poster"
DIFF_FILE_NAME=$1
post_review
