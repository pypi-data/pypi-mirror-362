# Jira CLI

A command-line interface for interacting with Jira.

This project uses [UV](https://github.com/astral-sh/uv) for dependency management.

## Installation

```bash
pip install cac-jira
```

## Authentication

On first-run, you'll be prompted for a Jira API token; generate one [here](https://id.atlassian.com/manage-profile/security/api-tokens). This will be stored in your system credential store (e.g. Keychain on Mac OS) in an items called `cac-jira`.

## Configuration

On first-run, a configuration file will be generated at `~/.config/cac_jira/config.yaml`. In this file you'll need to replace the values of `server` and `username` with appropriate values.

```yaml
server: https://your-jira-instance.atlassian.net
project: YOUR_PROJECT_KEY  # Optional default project
username: your.email@example.com
```

## Usage

The Jira CLI follows a command-action pattern for all operations:

```bash
jira <command> <action> [options]
```

### Global Options

- `--verbose`: Enable debug output
- `--output [table|json]`: Control output format (default table)
- `--help`: Show command help
<!-- --suppress-output: Hide command output -->
<!-- --version: Display version information -->

### Examples

#### Issue Commands

List issues in a project:

```bash
jira issue list --project PROJ
```

List issues with additional filtering:

```bash
jira issue list --project PROJ
```

Create a new issue:

```bash
jira issue create --project PROJ --type Task --title "Fix login bug" --description "Users can't log in"
```

Create a new issue of a type that requires custom fields:

```bash
#
# This assumes the name of the custom fields is "Custom Field One" and "Custom Field Two";
# the field name will be swapped to lower-case, and spaces replaced with underscores
#
jira issue create --project PROJ --type Custom\ Issue\ Type --title "Issue Title" --description "Issue description" \
  --field custom_field_one custom_field_value \
  --field custom_field_two custom_field_value
```

Create and assign to yourself:

```bash
jira issue create --project PROJ --type Bug --title "Server crash" --assign
```

Create and immediately start work:

```bash
jira issue create --project PROJ --type Story --title "Add login feature" --begin
```

Add an issue to an epic:

```bash
jira issue create --project PROJ --type Task --title "Subtask" --epic PROJ-100
```

Label an issue:

```bash
jira issue label --issue ISSUE_KEY --labels label1,label2
```

Transition an issue:

```bash
jira issue begin --issue ISSUE_KEY    # Start work
jira issue close --issue ISSUE_KEY    # Mark as complete
```

#### Project Commands

List all projects:

```bash
jira project list
```

Show a project:

```bash
jira project show --name PROJ-123
```

#### Advanced Examples

Update an issue's title or description:

```bash
jira issue update --issue ISSUE_KEY --title "New issue title" --description "new issue description"
```

Add a comment to an issue:

```bash
jira issue comment --issue ISSUE_KEY --comment "This is a comment."
```

List all issue IDs matching a label:

```bash
jira issue list --output json | jq -r '.[] | select(.Labels | contains("production")) | .ID'
```

## Development

### Setup Development Environment

```bash
# Install dependencies including dev dependencies
uv sync

# Activate the venv
source .venv/bin/activate

# Run tests
uv run pytest
```

Please note that tests are still WIP

### Project Structure

- `cac_jira/commands/` - Command implementations
  - `issue/` - Issue-related commands
  - `project/` - Project-related commands
- `cac_jira/cli/` - CLI entry point and argument parsing

### Adding New Commands

1. Create a new action module in the appropriate command directory.
2. Define a class that inherits from the command's base class.
3. Implement `define_arguments()` and `execute()` methods.
