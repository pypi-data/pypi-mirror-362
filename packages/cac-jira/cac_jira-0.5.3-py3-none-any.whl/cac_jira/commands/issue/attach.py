#!/usr/bin/env python
# pylint: disable=line-too-long, import-outside-toplevel, broad-exception-caught

"""
Command module for attaching files to Jira issues.
"""

from cac_jira.commands.issue import JiraIssueCommand


class IssueAttach(JiraIssueCommand):
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
        return parser

    def execute(self, args):
        raise NotImplementedError("This command is not implemented yet.")
