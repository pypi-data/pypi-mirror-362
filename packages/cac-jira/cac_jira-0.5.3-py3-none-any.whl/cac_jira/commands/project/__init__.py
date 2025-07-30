#!/usr/bin/env python
# pylint: disable=import-outside-toplevel
"""

Base module for all project-related commands.

This module defines the base ProjectCommand class that all project-related
action classes should inherit from.
"""

import abc
from cac_jira.commands.command import JiraCommand


class JiraProjectCommand(JiraCommand):
    """
    Base class for all project-related actions.

    This class defines common methods and properties that should be shared
    across all project actions, such as project-specific arguments and utilities.
    """
    @abc.abstractmethod
    def define_arguments(self, parser):
        """
        Define arguments specific to this command.

        Args:
            parser: The argument parser to add arguments to

        Returns:
            The modified parser
        """
        super().define_arguments(parser)
        # Add project-specific common arguments
        parser.add_argument(
            "-n",
            "--name",
            help="Filter projects by name (case-insensitive, partial match)",
            default=None,
        )
        parser.add_argument(
            "-k",
            "--key",
            help="Filter projects by key (case-insensitive, partial match)",
            default=None,
        )
        return parser

    @abc.abstractmethod
    def execute(self, args):
        """
        Execute the command with the provided arguments.

        Args:
            args: The parsed command line arguments

        Returns:
            Command result
        """
        # This method is meant to be overridden by specific project commands
        raise NotImplementedError("Subclasses must implement execute()")

    def get_project_types(self):
        """
        Get available project types.

        Returns:
            List of project types
        """
        # This is a placeholder - in a real implementation, this would
        # fetch actual project types from the Jira API
        self.log.debug("Getting project types")
        return ["software", "business", "service_desk"]

    def get_project_templates(self):
        """
        Get available project templates.

        Returns:
            Dictionary of project templates
        """
        # Placeholder implementation
        self.log.debug("Getting project templates")
        return {
            "scrum": "Template for Scrum projects",
            "kanban": "Template for Kanban projects",
            "basic": "Basic project with no specific methodology"
        }
