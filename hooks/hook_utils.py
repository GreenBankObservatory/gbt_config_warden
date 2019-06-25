"""Utility functions/constants for commit hooks"""

from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
import getpass
import os
import smtplib
import socket
import subprocess
import sys
import traceback

import pytz

# Get the full path of the repo executing this hook
GBT_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent

NOW = datetime.now(pytz.timezone("US/Eastern")).strftime("%Y-%m-%d %H:%M %Z")


def email(subject, text):
    """Send an email to SDD with given subject and text"""

    message = EmailMessage()
    message["Subject"] = subject
    # message["To"] = "GBO SDD <sddev@nrao.edu>"
    message["To"] = ",".join(
        check_output(["git", "config", "--get-all", "gbtconfig.recipient"]).split("\n")
    )
    message["From"] = check_output(["git", "config", "--get", "gbtconfig.from"])
    message["Reply-To"] = check_output(["git", "config", "--get", "gbtconfig.replyto"])

    message.set_content(text)
    if not DEBUG:
        try:
            smtplib.SMTP("smtp.gb.nrao.edu").send_message(message)
        except socket.gaierror:
            full_traceback = traceback.format_exc()
            print(
                f"Failed to send email to '{message['To']}'. Please manually send "
                f"an email to '{message['To']}' to let them know that this is broken. "
                "Include the following information:\n"
                f"{'='*80}\n{full_traceback}\n{'='*80}",
                file=sys.stderr,
            )
    else:
        print("\nThe following email would have been sent if DEBUG were False:")
        print("+" * 80)
        print(message)
        print("+" * 80)


def check_output(cmd_list):
    result = subprocess.check_output(cmd_list)
    # Convert from bytestring to UTF-8 and trim off newline
    result = result.decode("utf-8").strip()
    return result


def derive_user():
    return getpass.getuser()


def derive_branch():
    """Derive the git branch of the current repository"""

    try:
        branch = check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    except subprocess.CalledProcessError as error:
        raise ValueError(
            "Could not determine current branch! "
            "Please contact sddev@nrao.eu with this error message!"
        ) from error
    return branch


def derive_git_author():
    """Derive the current git author"""

    return os.environ.get("GIT_AUTHOR_NAME", None)


# Set to True for testing; this avoids sending emails
DEBUG = check_output(["git", "config", "--get", "gbtconfig.debug"]) == "true"
