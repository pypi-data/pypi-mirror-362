#!/usr/bin/env python
# pylint: disable=line-too-long, import-outside-toplevel, broad-exception-caught

"""
Command module for opening a Jira issue in a web browser.
"""

import webbrowser
from cac_jira.commands.issue import JiraIssueCommand


class IssueBrowse(JiraIssueCommand):
    """
    Command class for creating Jira issues.
    """

    def define_arguments(self, parser):
        """
        Define command-specific arguments.

        Args:
            parser: The argument parser to add arguments to
        """
        super().define_arguments(parser)
        parser.add_argument(
            "-i",
            "--issue",
            help="Issue to match",
            default=None,
            required=True,
        )
        return parser

    def execute(self, args):
        self.log.debug("Opening Jira issue %s in a browser", args.issue)
        issue = self.jira_client.issue(args.issue)
        webbrowser.open(issue.permalink())
