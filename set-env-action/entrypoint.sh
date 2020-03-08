#!/bin/sh -l

# Set ENV
if [[ $GITHUB_REF = "refs/heads/master" ]]
then
    export ENV="ops"
else
    export ENV="example"
fi

# Set Action output vars
echo ::set-output name=env::$ENV
