# #!/usr/bin/env python
# pylint: disable=no-member

from cac_jira.commands.issue import JiraIssueCommand

class IssueComment(JiraIssueCommand):
    """
    Command class for commenting on Jira issues.
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
        parser.add_argument(
            "-c",
            "--comment",
            help="Comment to add",
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
        self.log.debug("Commenting on Jira issue %s", args.issue)
        self.jira_client.add_comment(args.issue, args.comment)
        self.log.info("Added comment to %s", args.issue)
