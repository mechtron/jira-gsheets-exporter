#!/usr/bin/env python3

from jira import get_project_issues


def main():
    get_project_issues("OPS")


def handler(event, context):
    main()


if __name__ == "__main__":
    main()
