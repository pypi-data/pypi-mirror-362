# #!/usr/bin/env python
# pylint: disable=no-member

from cac_jira.commands.issue import JiraIssueCommand

class IssueAssign(JiraIssueCommand):
    """
    Command class for assigning Jira issues.
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
        self.log.debug("Assigning Jira issue %s to %s", args.issue, self.config.username)
        self.jira_client.assign_issue(args.issue, self.config.username)
        self.log.info("Issue assigned")
