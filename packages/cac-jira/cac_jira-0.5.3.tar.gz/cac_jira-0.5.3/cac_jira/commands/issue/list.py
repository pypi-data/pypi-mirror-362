#!/usr/bin/env python
# pylint: disable=line-too-long

"""
Command module for listing Jira issues.
"""

# import argparse
from datetime import datetime
import cac_core as cac
from cac_jira.commands.issue import JiraIssueCommand


class IssueList(JiraIssueCommand):
    """
    Command class for listing Jira issues.
    """

    def define_arguments(self, parser):
        """
        Define command-specific arguments.

        Args:
            parser: The argument parser to add arguments to
        """
        # Add common arguments first
        super().define_arguments(parser)
        parser.add_argument("-m", "--mine", action="store_true", default=False, help="List issues assigned to the current user")
        parser.add_argument("-d", "--done", action="store_true", default=False, help="Include issues that are done")

        return parser

    def execute(self, args):
        """
        Execute the command with the provided arguments.

        Args:
            args: The parsed arguments
        """
        self.log.debug("Listing Jira issues")

        # Build JQL query based on provided filters
        jql_parts = [f"project = {args.project}"]
        # if args.assignee:
        #     jql_parts.append(f"assignee = {args.assignee}")
        # if args.status:
        #     jql_parts.append(f"status = '{args.status}'")
        if args.mine:
            jql_parts.append("assignee = currentUser()")
        if not args.done:
            jql_parts.append("status != Done")

        # TODO: add start and end date filters
        # if args.start_date:
        #     jql_parts.append(f"resolutiondate >= '{args.start_date}'")
        # if args.end_date:
        #     jql_parts.append(f"resolutiondate <= '{args.end_date}'")
        # if args.labels:
        #     jql_parts.append(f"labels = {args.labels}")

        jql = " AND ".join(jql_parts) if jql_parts else ""
        self.log.debug("JQL query: %s", jql)
        total_issues = self.jira_client.search_issues(jql)

        models = []
        for issue in total_issues:
            assignee = issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned'
            resolution_date = datetime.strptime(issue.fields.resolutiondate, '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d') if issue.fields.resolutiondate else 'N/A'

            model = cac.model.Model(
                {
                    "ID": issue.key,
                    "Summary": issue.fields.summary,
                    "Status": issue.fields.status.name,
                    "Assignee": assignee,
                    "Issue Type": issue.fields.issuetype.name,
                    "Labels": ", ".join(issue.fields.labels),
                    "Resolution Date": resolution_date,
                }
            )
            models.append(model)

        printer = cac.output.Output(args)
        printer.print_models(models)
