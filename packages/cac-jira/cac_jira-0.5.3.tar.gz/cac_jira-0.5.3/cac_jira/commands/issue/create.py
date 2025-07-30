#!/usr/bin/env python
# pylint: disable=line-too-long, import-outside-toplevel, broad-exception-caught

"""
Command module for creating Jira issues.
"""

import webbrowser
from cac_jira.commands.issue import JiraIssueCommand

class IssueCreate(JiraIssueCommand):
    """
    Command class for creating Jira issues.
    """

    def define_arguments(self, parser):
        """
        Define command-specific arguments.

        Args:
            parser: The argument parser to add arguments to
        """
        # Add common arguments first
        super().define_arguments(parser)

        # Add action-specific arguments
        parser.add_argument(
            "-t",
            "--title",
            help="Issue title",
            required=True
        )
        parser.add_argument(
            "-d",
            "--description",
            help="Issue description",
            required=True
        )

        # TODO: get list of valid types from Jira
        parser.add_argument(
            "--type",
            help="Issue type (Bug, Task, Story, etc.)",
            default="Task"
        )

        # parser.add_argument(
        #     "--assignee",
        #     help="Assign the issue to a user",
        #     default=None
        # )

        parser.add_argument(
            "--assign",
            help="'Assign the issue to yourself?",
            action="store_true",
            default=False
        )

        parser.add_argument(
            "--begin",
            help="Mark issue in-progress",
            action="store_true",
            default=False
        )

        parser.add_argument(
            "--epic",
            help="Tie this issue to an existing Epic",
            default=None
        )

        parser.add_argument(
            "--labels",
            help="A comma-separated list of labels to apply to the issue",
            default=None
        )

        parser.add_argument(
            "--epic_name", help="Name your Epic", default=None
        )

        parser.add_argument(
            "--browse", help="Open the issue in your browser once created", action="store_true", default=False
        )

        # Add a custom argument for additional fields
        parser.add_argument(
            "--field",
            action="append",
            nargs=2,
            metavar=("FIELD_ID", "VALUE"),
            help="Specify custom field values in the format: --field fieldId value",
            dest="custom_fields"
        )

        return parser

    def get_mandatory_fields(self, project_key, issuetype_name):
        """
        Get mandatory fields for a specific issue type in a project.

        Args:
            project_key (str): Project key (e.g., 'TEST')
            issuetype_name (str): Issue type name (e.g., 'Bug', 'Task')

        Returns:
            dict: Dictionary of field_id -> field_name for mandatory fields
        """
        self.log.debug(f"Getting mandatory fields for {issuetype_name} in {project_key}")

        # Get the create metadata for this project and issue type
        metadata = self.jira_client.createmeta(
            projectKeys=project_key,
            issuetypeNames=issuetype_name,
            expand='projects.issuetypes.fields'
        )

        # Extract the fields from the metadata
        mandatory_fields = {}

        try:
            # Navigate the nested structure to get to the fields
            project_meta = metadata['projects'][0]
            issuetype_meta = project_meta['issuetypes'][0]
            fields = issuetype_meta['fields']

            # Identify mandatory fields (required=True)
            for field_id, field_info in fields.items():
                if field_info.get('required', False):
                    mandatory_fields[field_id] = {
                        'name': field_info['name'],
                        'schema': field_info.get('schema', {}),
                        'allowed_values': field_info.get('allowedValues', []),
                    }

            return mandatory_fields
        except (IndexError, KeyError) as e:
            self.log.error(f"Error parsing metadata: {e}")
            return {}

    def execute(self, args):
        """
        Execute the command with the provided arguments.

        Args:
            args: The parsed arguments
        """
        if args.begin:
            args.assign = True
        # Validate project is provided (required for issue creation)
        if not args.project:
            self.log.error("Project key is required for issue creation")
            return 1

        # validate project
        try:
            project = self.jira_client.project(args.project)
            self.log.debug("Project %s found", project.key)
        except Exception as e:
            self.log.error("Failed to find project %s: %s", args.project, e)
            return 1

        # validate issue type
        try:
            project = self.jira_client.project(args.project)
            # Get all issue types for the project
            issuetypes = project.issueTypes

            # Find the matching issue type
            matching_issuetype = None
            valid_types = []
            for issuetype in issuetypes:
                valid_types.append(issuetype.name)
                if issuetype.name.lower() == args.type.lower():
                    matching_issuetype = {"name": issuetype.name}
                    break

            if matching_issuetype is None:
                raise ValueError(f"Invalid issue type '{args.type}' for project '{args.project}'\nValid issue types are: {', '.join(valid_types)}")

        except Exception as e:
            print(f"Error: {e}")
            return

        # Prepare the issue data
        fieldset = {
            "project": args.project,
            "summary": args.title,
            "description": args.description,
            "issuetype": matching_issuetype,
            "reporter": {"accountId": self.jira_client.current_user()},
        }

        if args.labels:
            self.log.debug("Adding labels: %s", args.labels)
            fieldset['labels'] = args.labels.split(',')

        if args.epic:
            epic = self.jira_client.issue(args.epic).key
            self.log.debug("Adding to epic: %s", epic)
            fieldset["parent"] = {"key": epic}

        # if args.assignee:
        #     issue_data["assignee"] = args.assignee

        # TODO: handle epic creation
        # # If creating an epic, an epic name is required
        # if args.type == 'Epic':
        #     if args.epic_name is None:
        #         self.log.error("Epic Name is required if creating an Epic")
        #         return 1
        #     else:
        #         epic_name_field = self.jira_client.Field.all().select(lambda f: f.name == 'Epic Name').first().id
        #         fieldset[epic_name_field] = args.epic_name

        mandatory_fields = self.get_mandatory_fields(args.project, matching_issuetype["name"])

        # Create a mapping from field names to field IDs (both lowercase for case-insensitive matching)
        field_name_to_id = {}
        for field_id, field_info in mandatory_fields.items():
            field_name_to_id[field_info['name'].lower().replace(" ", "_")] = field_id

        # Print the mandatory fields
        if mandatory_fields:
            self.log.debug(f"Mandatory fields for {matching_issuetype['name']} in {args.project}:")
            for field_id, field_info in mandatory_fields.items():
                self.log.debug(f"  {field_info['name'].lower().replace(" ", "_")} ({field_id})")

        # Apply individual field arguments
        if args.custom_fields:
            for field_name_or_id, value in args.custom_fields:
                # First check if this is a field name
                field_id = field_name_or_id

                # Try to match the field name (case-insensitive)
                if field_name_or_id.lower() in field_name_to_id:
                    field_id = field_name_to_id[field_name_or_id.lower()]
                    self.log.debug(f"Mapped field name '{field_name_or_id}' to ID '{field_id}'")

                # Handle special field types
                if field_id.startswith("customfield_"):
                    # Try to determine field type from schema
                    field_schema = mandatory_fields.get(field_id, {}).get('schema', {})
                    field_type = field_schema.get('type')

                    if field_type == 'array':
                        # Handle array fields by splitting on comma
                        fieldset[field_id] = value.split(',')
                    elif field_type == 'option':
                        # Handle option fields
                        fieldset[field_id] = {'value': value}
                    else:
                        fieldset[field_id] = value
                else:
                    fieldset[field_id] = value

        # Check if we have all mandatory fields
        missing_fields = []
        for field_id, field_info in mandatory_fields.items():
            # Skip fields that we already handle (summary, description, project, issuetype, reporter)
            if field_id in ['summary', 'description', 'project', 'issuetype', 'reporter']:
                continue

            # Check if this mandatory field is missing
            if field_id not in fieldset:
                missing_fields.append(f"{field_info['name'].lower().replace(" ", "_")} ({field_id})")

        # If there are missing mandatory fields, warn the user
        if missing_fields:
            raise ValueError(f"Missing mandatory fields: {', '.join(missing_fields)}")

        self.log.debug("Issue data: %s", fieldset)
        issue = self.jira_client.create_issue(fields=fieldset)
        self.log.info("Issue %s created successfully", issue.key)

        if args.assign:
            issue.update(assignee={"accountId": self.jira_client.current_user()})
            self.log.info("Issue %s assigned to you", issue.key)

        if args.begin:
            try:
                # Import the begin command module
                from cac_jira.commands.issue.begin import IssueBegin

                # Create a begin command instance
                begin_cmd = IssueBegin()

                # Prepare args for the begin command
                # We need to simulate args with an 'issue' attribute containing the new issue key
                from argparse import Namespace
                begin_args = Namespace(issue=issue.key)

                # Execute the begin command with our constructed args
                begin_cmd.execute(begin_args)
            except Exception as e:
                self.log.error("Failed to transition issue to In Progress: %s", str(e))

        if args.browse:
            webbrowser.open(issue.permalink())
