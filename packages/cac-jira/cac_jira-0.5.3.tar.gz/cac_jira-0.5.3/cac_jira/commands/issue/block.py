"""
Module for handling the blocking of Jira issues.

This module provides functionality to transition Jira issues to a "Blocked" state,
allowing users to mark issues that cannot proceed due to dependencies or other obstacles.
Users can optionally add a comment explaining why the issue is being blocked.
"""

# pylint: disable=broad-exception-caught

from cac_jira.commands.issue import JiraIssueCommand


class IssueBlock(JiraIssueCommand):
    """
    Command class for transitioning Jira issues to "Blocked".
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
            help="Issue to transition to Blocked",
            default=None,
            required=True,
        )
        parser.add_argument(
            "-c",
            "--comment",
            help="Comment to add when transitioning to Blocked",
            default=None,
            required=False,
        )
        return parser

    def execute(self, args):
        """
        Execute the command with the provided arguments.

        Args:
            args: The parsed arguments
        """
        self.log.debug("Transitioning Jira issue %s to Blocked", args.issue)

        # Get the issue
        issue = self.jira_client.issue(args.issue)
        if not issue:
            self.log.error("Issue not found")
            return

        # Get all available transitions for the issue
        transitions = self.jira_client.transitions(issue)

        # Find the transition ID where name is "Blocked" (case-insensitive)
        transition_id = None
        transition_name = None
        desired_transition = "Blocked"
        for transition in transitions:
            if transition["name"].upper() == desired_transition.upper():
                transition_id = transition['id']
                transition_name = transition['name']
                self.log.debug(
                    "Found '%s' transition with ID: %s", transition_name, transition_id
                )
                break

        if not transition_id:
            self.log.error("No '%s' transition found for this issue", desired_transition)
            # List all available transitions
            self.log.info("Available transitions:")
            for transition in transitions:
                self.log.info("  - %s (ID: %s)", transition['name'], transition['id'])
            return

        # Transition the issue to "Blocked"
        try:
            self.jira_client.transition_issue(issue, transition_id)
            if args.comment:
                self.jira_client.add_comment(issue, args.comment)
                self.log.info('Added comment: "%s"', args.comment)
            self.log.info('Issue %s transitioned to "%s"', issue.key, transition_name)
        except Exception as e:
            self.log.error("Failed to transition issue: %s", str(e))
