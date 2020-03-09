#!/bin/sh -l

set -e

# Set ENV
if [[ $GITHUB_REF = "refs/heads/master" ]]
then
    export ENV="prod"
else
    export ENV="test"
fi

# Set Action output vars
echo ::set-output name=env::$ENV
