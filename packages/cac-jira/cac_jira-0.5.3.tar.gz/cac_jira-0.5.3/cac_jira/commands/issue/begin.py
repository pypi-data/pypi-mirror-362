"""
Module for handling the start of work on Jira issues.

This module provides functionality to transition Jira issues to an "In Progress" state,
indicating that work has begun on the issue. This allows teams to track which issues
are actively being worked on and by whom.
"""

# pylint: disable=broad-exception-caught

from cac_jira.commands.issue import JiraIssueCommand


class IssueBegin(JiraIssueCommand):
    """
    Command class for transitioning Jira issues to "In Progress".
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
            help="Issue to transition to In Progress",
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
        self.log.debug("Transitioning Jira issue %s to In Progress", args.issue)

        # Get the issue
        issue = self.jira_client.issue(args.issue)
        if not issue:
            self.log.error("Issue not found")
            return

        # Get all available transitions for the issue
        transitions = self.jira_client.transitions(issue)

        # Find the transition ID where name is "In Progress"
        transition_id = None
        transition_name = None
        desired_transition = "In Progress"
        for transition in transitions:
            if transition['name'].upper() == desired_transition.upper():
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

        # Transition the issue to "In Progress"
        try:
            self.jira_client.transition_issue(issue, transition_id)
            self.log.info('Issue %s transitioned to "%s"', issue.key, transition_name)
        except Exception as e:
            self.log.error("Failed to transition issue: %s", str(e))
