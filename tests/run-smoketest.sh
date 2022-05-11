#!/bin/bash

set -e

TEST_REPOS=(
    "https://github.com/sqlalchemy/sqlalchemy/zipball/rel_1_4_36/"
    "https://github.com/psf/requests/zipball/v2.27.1/"
    "https://github.com/PyCQA/flake8/zipball/4.0.1/"
)

mkdir -p .smoketest

for TEST_REPO in ${TEST_REPOS[@]}
do
    echo "Running smoke test on repo $TEST_REPO";

    cd .smoketest
	wget -qO repo.zip $TEST_REPO
    unzip -qq repo.zip -d repo/
    flake8 repo/ &> result.log || true

    if grep -r "Traceback (most recent call last)" -A 50 result.log; then
        echo "Smoke test failed on repo $TEST_REPO";
        exit 1
    else
        echo "Smoke test succeded on repo $TEST_REPO";
        echo "Here are a few issues found in the test repo: ";
        echo -e "\n"
        grep -E "JG[0-9][0-9]" result.log | head -n 20
        echo -e "\n"
    fi

    rm -rf repo repo.zip result.log
    cd ..
done
