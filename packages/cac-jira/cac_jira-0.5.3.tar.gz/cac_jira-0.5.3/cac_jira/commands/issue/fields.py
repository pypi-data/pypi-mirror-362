#!/usr/bin/env python
# pylint: disable=line-too-long, import-outside-toplevel, broad-exception-caught

"""
Command module for listing mandatory fields for Jira issue types.
"""

# import webbrowser
from cac_jira.commands.issue import JiraIssueCommand

class IssueFields(JiraIssueCommand):
    """
    Command class for displaying required fields for issue creation.
    """

    def define_arguments(self, parser):
        super().define_arguments(parser)
        parser.add_argument(
            "--type",
            help="Issue type to check fields for",
            default=None
        )
        return parser

    def execute(self, args):
        """List required fields for issue creation"""
        project = args.project
        issuetype = args.type

        # Get create metadata
        metadata = self.jira_client.createmeta(
            projectKeys=project,
            issuetypeNames=issuetype,
            # expand='projects.issuetypes.fields'
        )

        try:
            project_meta = metadata['projects'][0]

            # If no specific issue type, list all types
            if not issuetype:
                print(f"\nAvailable issue types for {project}:")
                for it in project_meta['issuetypes']:
                    print(f"  {it['name']}")
                return

            # Find specific issue type
            issuetype_meta = None
            for it in project_meta['issuetypes']:
                if it['name'].lower() == issuetype.lower():
                    issuetype_meta = it
                    break

            if not issuetype_meta:
                print(f"Issue type '{issuetype}' not found in project {project}")
                return

            print(f"\nRequired fields for {issuetype} in {project}:")
            for field_id, field in issuetype_meta['fields'].items():
                if field.get('required', False):
                    allowed = ""
                    if 'allowedValues' in field and field['allowedValues']:
                        values = [v.get('name', v.get('value', 'Unknown'))
                                 for v in field['allowedValues'][:5]]
                        allowed = f" (Options: {', '.join(values)}{'...' if len(field['allowedValues']) > 5 else ''})"

                    print(f"  {field['name']}{allowed} ({field_id})")

            print("\nOptional fields:")
            for field_id, field in issuetype_meta['fields'].items():
                if not field.get('required', False):
                    print(f"  {field['name']} ({field_id})")

        except (IndexError, KeyError) as e:
            print(f"Error retrieving field information: {e}")
