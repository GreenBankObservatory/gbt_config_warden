"""Sanity checks prior to commiting to GBT config repo

See README.md for notes on testing
"""

import sys
import traceback

from hook_utils import (
    derive_branch,
    derive_git_author,
    derive_user,
    email,
    GBT_CONFIG_PATH,
    NOW,
    check_output,
)


# The current "release" branch. This will need to be changed on each M&C release
PRIMARY_BRANCH = check_output(["git", "config", "--get", "gbtconfig.releasebranch"])
# This are a whitelist of users that are allowed to commit to the non-primary branch
WHITELISTED_USERS = check_output(["git", "config", "--get-all", "gbtconfig.whitelistuser"]).split("\n")
# These are authors that are not allowed for commits. These are bad because
# it hides information about who actually committed
BLACKLISTED_AUTHORS = check_output(["git", "config", "--get-all", "gbtconfig.blacklistauthor"]).split("\n")


def perform_precommit_sanity_checks(git_author_name, user, branch):
    """Sanity checks prior to commiting to GBT config repo"""
    if not git_author_name or git_author_name in BLACKLISTED_AUTHORS:
        if git_author_name:
            user_description = f"blacklisted author '{git_author_name}'"
        else:
            user_description = "an unknown author (blank GIT_AUTHOR_NAME)"

        raise ValueError(
            f"Commits are not allowed to be authored by {user_description}! You must either:\n"
            "  * Commit again under your own personal user account\n"
            "  * Commit again using --author=<your_name>"
        )

    if branch != PRIMARY_BRANCH and user not in WHITELISTED_USERS:
        raise ValueError(
            f"You are attempting to commit to non-primary branch '{branch}' "
            f"as user '{user}'.\nThis is not allowed: as an unprivileged "
            f"user, you may only commit to primary branch '{PRIMARY_BRANCH}'.\n"
            "You will need to wait for SDD to switch back to the primary branch "
            "before you commit your code."
        )


def main():
    """CLI Main"""

    git_author_name = derive_git_author()
    user = derive_user()
    branch = None
    try:
        branch = derive_branch()
        perform_precommit_sanity_checks(git_author_name, user, branch)
    # This is purposefully broad: we want to catch any possible error here so
    # that an email can be sent to SDD explaining what happened. The entire
    # traceback will be captured
    # pylint: disable=broad-except
    except Exception as error:
        full_traceback = traceback.format_exc()
        error_msg = f"ERROR: {error}\nNO CODE HAS BEEN COMMITTED!"
        print(error_msg, file=sys.stderr)
        subject = (
            f"GBT Config Warden: User '{user}' has attempted to commit "
            f"files to {GBT_CONFIG_PATH}"
        )
        email_text = (
            f"User '{user}' attempted to commit code as author '{git_author_name}' to active branch "
            f"'{branch}' of '{GBT_CONFIG_PATH}' on {NOW}. They were prevented from doing so, "
            f"and shown the following error message:\n"
            f"{'='*80}\n{error_msg}\n{'='*80}\n\n"
            f"Below is debug info:\n\n"
            f"Global variables:\n"
            f"  PRIMARY_BRANCH: {PRIMARY_BRANCH}\n"
            f"  WHITELISTED_USERS: {WHITELISTED_USERS}\n"
            f"  BLACKLISTED_AUTHORS: {BLACKLISTED_AUTHORS}\n"
            f"\n\nFull traceback:\n"
            f"{'='*80}\n{full_traceback}\n{'='*80}\n\n"
            "Reminder: to make changes to the above variables, you need to edit the git config!\n"
            "See \"$ git config --local --list | grep '^gbtconfig\\.'\" for more details."
        )

        email(subject=subject, text=email_text)
        sys.exit(1)


if __name__ == "__main__":
    main()
