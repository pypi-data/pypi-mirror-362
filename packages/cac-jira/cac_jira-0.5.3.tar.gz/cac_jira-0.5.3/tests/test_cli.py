#!/usr/bin/env python

"""
Test script for the Jira CLI implementation.

This script provides examples of how to use the Jira CLI by directly
invoking different commands and actions.
"""

import sys
import argparse
from cac_jira.cli.main import main
from cac_jira.commands.issue import JiraIssueCommand
from cac_jira.commands.issue.list import IssueList
from cac_jira.commands.issue.create import IssueCreate
from cac_jira.commands.project import JiraProjectCommand
from cac_jira.commands.project.list import ProjectList

def test_cli_direct():
    """Test the CLI by directly calling the main function with different arguments."""
    print("\n==== Testing CLI through main() function ====")

    # Test 1: Issue list command
    print("\n-- Testing 'jira issue list' command --")
    sys.argv = ["jira", "issue", "list", "--project", "TEST"] #, "--limit", "5"] #, "--verbose"]
    main()

    # Test 2: Project list command
    print("\n-- Testing 'jira project list' command --")
    sys.argv = ["jira", "project", "list"] #, "--archived"] #, "--verbose"]
    main()

    # # Test 3: Issue create command
    # print("\n-- Testing 'jira issue create' command --")
    # sys.argv = ["jira", "issue", "create", "--project", "TEST", "--summary", "Test Issue"] #, "--verbose"]
    # main()

def test_command_classes():
    """Test by directly instantiating and using command classes."""
    print("\n==== Testing command classes directly ====")

    # Test IssueList command
    print("\n-- Testing IssueList command --")
    issue_list = IssueList()
    parser = argparse.ArgumentParser()
    issue_list.define_arguments(parser)
    args = parser.parse_args(["--project", "TEST"]) #, "--limit", "10"]) #, "--server", "https://jira.example.com"])
    issue_list.execute(args)

    # # Test ProjectList command
    # print("\n-- Testing ProjectList command --")
    # project_list = ProjectList()
    # parser = argparse.ArgumentParser()
    # project_list.define_arguments(parser)
    # args = parser.parse_args(["--archived", "--type", "software", "--server", "https://jira.example.com"])
    # project_list.execute(args)

    # Test ProjectList command
    print("\n-- Testing ProjectList command --")
    project_list = ProjectList()
    parser = argparse.ArgumentParser()
    project_list.define_arguments(parser)
    args = parser.parse_args(["--name", "crdb"])
    project_list.execute(args)

    # # Test IssueCreate command
    # print("\n-- Testing IssueCreate command --")
    # issue_create = IssueCreate()
    # parser = argparse.ArgumentParser()
    # issue_create.define_arguments(parser)
    # args = parser.parse_args([
    #     "--project", "TEST",
    #     "--summary", "Test Issue via Direct Call",
    #     "--description", "This is a test issue created by directly calling the command class",
    #     "--priority", "High",
    #     "--server", "https://jira.example.com"
    # ])
    # issue_create.execute(args)

def main_test():
    """Main test function."""
    print("Starting Jira CLI tests...")

    try:
        # Test using the CLI main function
        test_cli_direct()
    except Exception as e:
        print(f"Error testing via CLI main(): {e}")

    try:
        # Test using direct class instantiation
        test_command_classes()
    except Exception as e:
        print(f"Error testing via direct class instantiation: {e}")

    print("\nTest completed.")

if __name__ == "__main__":
    main_test()
