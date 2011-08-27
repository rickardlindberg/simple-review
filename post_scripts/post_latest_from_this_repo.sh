#!/bin/sh

NUM=5
FILE=tmp.diff

post_review() {
    curl \
        --data-urlencode "name=${message}" \
        --data-urlencode "user=${author}" \
        --data-urlencode "diff@${FILE}" \
        http://localhost:8080/create_review
}

for rev in $(git log -$NUM | grep ^commit | awk '{ print $2 }'); do
    git diff ${rev}^ $rev > $FILE
    message=$(git show -s --format=format:%s ${rev}^{commit})
    author=$(git show -s --format=format:%cn ${rev}^{commit})
    post_review
done;

rm $FILE
