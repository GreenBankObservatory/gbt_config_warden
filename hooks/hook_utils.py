"""Utility functions/constants for commit hooks"""

from datetime import datetime
from email.message import EmailMessage
import getpass
import os
import smtplib
import socket
import subprocess
import sys
import traceback

import pytz

# Get the full path of the repo executing this hook

NOW = datetime.now(pytz.timezone("US/Eastern")).strftime("%Y-%m-%d %H:%M %Z")


def email(subject, text):
    """Send an email to SDD with given subject and text"""

    message = EmailMessage()
    message["Subject"] = subject
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

    branch = check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return branch


def derive_git_author():
    """Derive the current git author"""

    author = os.environ.get("GIT_AUTHOR_NAME", None)
    if not author:
        author = check_output(["git", "config", "user.name"])

    return author


def get_status():
    status = check_output(["git", "status", "--untracked-files=no", "--short"])
    if not status:
        return "<Clean status>"
    return status


def get_files_in_prev_commit():
    return check_output(["git", "diff", "--name-only", "HEAD~"])


def get_proc_file_reminder(files_in_prev_commit):
    proc_files_changed = [
        f"  * {line}"
        for line in files_in_prev_commit.split("\n")
        if line.strip().endswith("Proc.conf")
    ]
    proc_files_changed_str = "\n".join(proc_files_changed)
    if proc_files_changed:
        proc_file_reminder = (
            "NOTE: One or more *Proc.conf files has changed! "
            "Please consider doing a $ tm systemstop && tm systemstart on affected host(s)\n"
            f"{proc_files_changed_str}"
            "\n\n"
        )
    else:
        proc_file_reminder = ""

    return proc_file_reminder


def get_ref_name(hash):
    try:
        full_ref_name = check_output(
            ["git", "describe", hash, "--all", "--exact-match"]
        )
        return full_ref_name.split("/")[1]
    except Exception:
        print(f"Warning: failed to derive branch name for {hash!r}", file=sys.stderr)
        return hash


def get_changed_filenames(ref1, ref2):
    return check_output(["git", "diff", "--name-only", ref1, ref2])


def get_changes_since_last_commit():
    return check_output(["git", "diff", "HEAD~"])

def get_commit_log():
    return check_output(["git", "log", "HEAD^..HEAD"])


# Set to True for testing; this avoids sending emails
DEBUG = check_output(["git", "config", "--get", "gbtconfig.debug"]) == "true"
# Repo path
GBT_CONFIG_PATH = check_output(["git", "rev-parse", "--show-toplevel"])
