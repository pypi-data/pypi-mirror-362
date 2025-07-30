# pylint: disable=broad-except, line-too-long

"""
module docstring
"""

# import os
import sys
from importlib import metadata
import cac_core as cac
# import yaml
# import keyring
import cac_jira.core.client as client

if sys.version_info < (3, 9):
    print("This project requires Python 3.9 or higher.", file=sys.stderr)
    sys.exit(1)

cac.updatechecker.check_package_for_updates(__name__)

try:
    __version__ = metadata.version(__package__)
except Exception:
    __version__ = "#N/A"

log = cac.logger.new(__name__)
log.debug("Initializing %s version %s", __name__, __version__)

CONFIG = cac.config.Config(__name__)

log.debug("user config path: %s", CONFIG.config_file)

# TODO: prompt user for server and username if not set
jira_server = CONFIG.get("server", "INVALID_DEFAULT").replace("https://", "")
if jira_server == "INVALID_DEFAULT":
    log.error("Invalid server in %s: %s", CONFIG.config_file, jira_server)
    sys.exit(1)

jira_username = CONFIG.get('username', 'INVALID_DEFAULT')
if jira_username == "INVALID_DEFAULT":
    log.error("Invalid username in %s: %s", CONFIG.config_file, jira_username)
    sys.exit(1)

credentialmanager = cac.credentialmanager.CredentialManager(__name__)
jira_api_token = credentialmanager.get_credential(
    jira_username,
    "Jira API key",
)

if not jira_api_token:
    log.error(
        "API token not found for %s; see https://github.com/rpunt/%s/blob/main/README.md#authentication",
        jira_username,
        __name__.replace("_", "-"),
    )
    sys.exit(1)

JIRA_CLIENT = client.JiraClient(jira_server, jira_username, jira_api_token)

__all__ = ["JIRA_CLIENT", "CONFIG", "log"]
