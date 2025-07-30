#!/usr/bin/env python
# pylint: disable=no-member

"""
Jira client module.
"""

import jira
import cac_core as cac

log = cac.logger.new(__name__)


class JiraClient:
    """
    Jira client class.
    """

    def __init__(self, server, username, api_token=None):
        """
        Initialize the Jira client.

        Args:
            server: The Jira server
            username: The Jira username
            api_token: The Jira API token
        """
        self.server = server
        self.username = username
        self.api_token = api_token
        self.client = None
        self.connect()

    def connect(self):
        """
        Connect to the Jira server.
        """
        log.debug("Connecting to Jira server %s", self.server)
        try:
            self.client = jira.JIRA(
                f"https://{self.server}",
                basic_auth=(self.username, self.api_token),
            )
        except Exception as e:
            log.error("Failed to connect to Jira server: %s", e)
            raise

    # Pass through methods to the Jira client
    def issue(self, issue_id):
        """
        Get an issue.

        Args:
            issue_id: The issue ID

        Returns:
            The issue
        """
        return self.client.issue(issue_id)

    def transitions(self, issue):
        """
        Get available transitions for an issue.

        Args:
            issue: The issue

        Returns:
            The available transitions
        """
        return self.client.transitions(issue)

    def transition_issue(self, issue_id, transition_id, **kwargs):
        """
        Transition an issue.

        Args:
            issue: The issue
            transition_id: The transition ID
            **kwargs: Additional arguments to pass to the transition
        """
        return self.client.transition_issue(issue_id, transition_id, **kwargs)

    def add_comment(self, issue_id, comment):
        """
        Add a comment to an issue.

        Args:
            issue: The issue to comment on
            comment: The comment text to add

        Returns:
            The created comment
        """
        return self.client.add_comment(issue_id, comment)

    def assign_issue(self, issue_id, username):
        """
        Assign an issue to a user.

        Args:
            issue: The issue to assign
            username: The username to assign the issue to

        Returns:
            The response from the assignment operation
        """
        return self.client.assign_issue(issue_id, username)

    def add_labels(self, issue_id, labels):
        """
        Add labels to an issue.

        Args:
            issue_id: The issue
            labels: The labels to add
        """
        issue = self.issue(issue_id)
        if not issue:
            log.error("Issue not found")
            return
        return issue.update(fields={"labels": labels.split(",")})

    def create_issue(self, **kwargs):
        """
        Create a new issue.

        Args:
            **kwargs: The fields to set on the new issue

        Returns:
            The created issue
        """
        return self.client.create_issue(**kwargs)

    def search_issues(self, jql):
        """
        Search for issues.

        Args:
            **kwargs: The search parameters

        Returns:
            The list of issues
        """
        # return self.client.search_issues(jql)
        start_at = 0
        max_results = 50  # Number of issues to fetch per request
        all_issues = []
        while True:
            issues = self.client.search_issues(
                jql,
                startAt=start_at,
                maxResults=max_results,
                fields=[
                    "key",
                    "summary",
                    "status",
                    "assignee",
                    "issuetype",
                    "labels",
                    "resolutiondate",
                ],
            )

            all_issues.extend(issues)

            # Break the loop if we've fetched all issues
            if len(issues) < max_results:
                break

            # Update startAt for the next batch
            start_at += max_results
            # TODO: this doesn't actually log, maybe the wrong logger?
            log.debug("Fetched %d issues", len(all_issues))
        return all_issues

    def delete_issue(self, issue_id):
        """
        Delete an issue.

        Args:
            issue_id: The issue ID

        Returns:
            The response from the delete operation
        """
        issue = self.issue(issue_id)
        if not issue:
            log.error("Issue not found")
            return
        return issue.delete()

    def projects(self):
        """
        Get all projects.

        Returns:
            The list of projects
        """
        return self.client.projects()

    def project(self, project_id):
        """
        Get a project.

        Args:
            project_id: The project ID

        Returns:
            The project
        """
        return self.client.project(project_id)
    def project_by_key(self, project_key):
        """
        Get a project by key.

        Args:
            project_key: The project key

        Returns:
            The project
        """
        return self.client.project_by_key(project_key)

    def current_user(self):
        """
        Get the current user.

        Returns:
            The current user
        """
        return self.client.current_user()

    def issue_types(self):
        """
        Get all issue types.
        """
        return self.client.issue_types()

    def issue_type(self, issue_type_id):
        """
        Get an issue type.
        """
        return self.client.issue_type(issue_type_id)

    def issue_type_by_name(self, name):
        """
        Get an issue type by name.
        """
        return self.client.issue_type_by_name(name)

    def issue_type_by_id(self, issue_type_id):
        """
        Get an issue type by ID.
        """
        return self.client.issue_type_by_id(issue_type_id)

    def issue_type_by_key(self, issue_type_key):
        """
        Get an issue type by key.
        """
        return self.client.issue_type_by_key(issue_type_key)

    def issue_type_by_project(self, project_id):
        """
        Get issue types by project ID.
        """
        return self.client.issue_type_by_project(project_id)
    def issue_type_by_project_key(self, project_key):
        """
        Get issue types by project key.
        """
        return self.client.issue_type_by_project_key(project_key)

    def add_issues_to_epic(self, epic_key, issue_key):
        """
        Add issues to an epic.

        Args:
            epic_key: The epic issue
            issue_key: The Jira key of the issue to add

        Returns:
            The response from the add operation
        """
        return self.client.add_issues_to_epic(epic_key, issue_key)

    def createmeta(self, projectKeys=None, issuetypeNames=None, expand=None):
        """
        Get create metadata for a project and issue type.
        Args:
            projectKeys: The project key (e.g., 'TEST')
            issuetypeNames: The issue type name (e.g., 'Bug', 'Task')
        Returns:
            The create metadata
        """
        return self.client.createmeta(
            projectKeys=projectKeys,
            issuetypeNames=issuetypeNames,
            expand=expand or 'projects.issuetypes.fields'
        )
    # def project(self, project_id):
    #     """
    #     Get a project.

    #     Returns:
    #         The project
    #     """
    #     return self.client.project(project_id)
