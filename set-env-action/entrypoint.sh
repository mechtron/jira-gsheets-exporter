#!/bin/sh -l

printenv

case $CIRCLE_BRANCH in
    "develop")
        export ENVIRONMENT="dev"
        ;;
    "staging")
        export ENVIRONMENT="staging"
        ;;
    "production")
        export ENVIRONMENT="production"
        ;;
esac

# Set Action output vars
echo ::set-output name=env::$ENVIRONMENT
