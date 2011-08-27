#!/bin/sh

SERVER="http://localhost:8080"
NUM_REVS_TO_INCLUDE=5
DIFF_FILE_NAME=tmp.diff

post_latest() {
    for rev in $(latest_revisions); do
        extract_review_data
        post_review
    done
    rm $DIFF_FILE_NAME
}

latest_revisions() {
    git log -${NUM_REVS_TO_INCLUDE} | grep ^commit | awk '{ print $2 }'
}

extract_review_data() {
    git diff ${rev}^ $rev > $DIFF_FILE_NAME
    message=$(git show -s --format=format:%s ${rev}^{commit})
    author=$(git show -s --format=format:%cn ${rev}^{commit})
}

post_review() {
    curl \
        --data-urlencode "name=${message}" \
        --data-urlencode "user=${author}" \
        --data-urlencode "diff@${DIFF_FILE_NAME}" \
        ${SERVER}/create_review
}

post_latest
