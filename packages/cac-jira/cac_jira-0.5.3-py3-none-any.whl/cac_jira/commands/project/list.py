"""
Command module for listing Jira projects.

This module provides functionality to list projects in Jira, with optional
filtering by name or key. It utilizes the JiraProjectCommand base class to
handle Jira connectivity and authentication.

Projects can be filtered by:
- Project name (case-insensitive substring matching)
- Project key (case-insensitive substring matching)

The results are displayed in a table format by default, or as JSON when
specified with the --output argument.

Example:
    jira project list
    jira project list --name "Core"
    jira project list --key "COR" --output json
"""

import cac_core as cac
from cac_jira.commands.project import JiraProjectCommand


class ProjectList(JiraProjectCommand):
    """
    Command class for listing Jira projects.
    """

    def define_arguments(self, parser):
        """
        Define command-specific arguments.

        Args:
            parser: The argument parser to add arguments to
        """
        super().define_arguments(parser)
        return parser

    def get_projects(self, args):
        """
        Get list of projects, optionally filtered.

        Args:
            args: The parsed arguments containing filter criteria

        Returns:
            list: List of project objects
        """
        self.log.debug("Listing all Jira projects")

        projects = self.jira_client.projects()  # pylint: disable=no-member
        if not projects:
            self.log.error("Projects not found")
            return []

        # Apply filters if provided
        filtered_projects = projects

        if getattr(args, 'name', None):
            name_filter = args.name.lower()
            filtered_projects = [p for p in filtered_projects if name_filter in p.name.lower()]

        if getattr(args, 'key', None):
            key_filter = args.key.lower()
            filtered_projects = [p for p in filtered_projects if key_filter in p.key.lower()]

        return filtered_projects

    def execute(self, args):
        """
        Execute the command with the provided arguments.

        Args:
            args: The parsed arguments
        """
        projects = self.get_projects(args)

        if not projects:
            self.log.error("No projects found")
            return

        # Convert to models for display
        models = []
        for project in projects:
            model = cac.model.Model(
                {"ID": project.id, "Key": project.key, "Name": project.name}
            )
            models.append(model)

        printer = cac.output.Output(args)
        printer.print_models(models)
