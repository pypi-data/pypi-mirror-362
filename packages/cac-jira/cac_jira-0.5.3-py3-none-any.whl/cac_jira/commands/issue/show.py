#!/usr/bin/env python
# pylint: disable=line-too-long, import-outside-toplevel, broad-exception-caught

"""
Command module for showing Jira issues.
"""

import json
import cac_core as cac
from cac_jira.commands.issue import JiraIssueCommand

class IssueShow(JiraIssueCommand):
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
        self.log.debug("Showing Jira issue %s", args.issue)
        issue = self.jira_client.issue(args.issue)
        if args.output == "json":
            # skip the model JSON output and just print the raw issue
            print(json.dumps(issue.raw, indent=4))
            return
        else:
            models = []
            model = cac.model.Model({
                "ID": issue.id,
                "Key": issue.key,
                "Summary": issue.fields.summary,
                "Status": issue.fields.status.name,
                "Type": issue.fields.issuetype.name,
                "Priority": issue.fields.priority.name
            })
            models.append(model)
            printer = cac.output.Output(args)
            printer.print_models(models)
