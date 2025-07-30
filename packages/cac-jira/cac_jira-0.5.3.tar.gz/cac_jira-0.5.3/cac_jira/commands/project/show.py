#!/usr/bin/env python

import cac_core as cac
from cac_jira.commands.project import JiraProjectCommand
from cac_jira.commands.project.list import ProjectList

class ProjectShow(JiraProjectCommand):
    """
    Command class for showing details of a specific Jira project.
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
        """
        Execute the command with the provided arguments.

        Args:
            args: The parsed arguments
        """
        # self.log.debug("Showing Jira project %s", args.project)

        # Use ProjectList to get the list of projects
        project_list = ProjectList()
        projects = project_list.get_projects(args)

        if not projects:
            self.log.error("Projects not found")
            return

        # Find project by key (case insensitive)
        models = []
        for project in projects:
            model = cac.model.Model(
                {"ID": project.id, "Key": project.key, "Name": project.name}
            )
            models.append(model)

        printer = cac.output.Output(args)
        printer.print_models(models)
