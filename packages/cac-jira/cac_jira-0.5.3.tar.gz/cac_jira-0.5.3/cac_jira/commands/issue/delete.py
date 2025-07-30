# #!/usr/bin/env python
# pylint: disable=broad-exception-caught

from cac_jira.commands.issue import JiraIssueCommand


class IssueDelete(JiraIssueCommand):
    """
    Command class for deleting Jira issues.
    """

    def define_arguments(self, parser):
        """
        Define command-specific arguments.

        Args:
            parser: The argument parser to add arguments to
        """
        # Add common arguments first
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
        """
        Execute the command with the provided arguments.

        Args:
            args: The parsed arguments
        """
        self.log.debug("Deleting Jira issue")
        try:
            self.jira_client.delete_issue(args.issue)
        except Exception as e:
            self.log.error("Failed to find issue %s: %s", args.issue, e)
            return
        self.log.info("Issue %s deleted", args.issue)
