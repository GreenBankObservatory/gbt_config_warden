"""Notify SDD after files are committed to GBT config repo"""

from hook_utils import (
    check_output,
    derive_branch,
    derive_git_author,
    derive_user,
    email,
    GBT_CONFIG_PATH,
    get_changes_since_last_commit,
    get_commit_log,
    get_files_in_prev_commit,
    get_proc_file_reminder,
    get_status,
    NOW,
)


def main():
    """CLI Main"""

    branch = derive_branch()
    git_author_name = derive_git_author()
    user = derive_user()

    changes_since_last_commit = get_changes_since_last_commit()
    commit_log = get_commit_log()
    status = get_status()
    proc_file_reminder = get_proc_file_reminder(get_files_in_prev_commit())

    subject = f"GBT Config Warden: Author '{git_author_name}' has committed files to {GBT_CONFIG_PATH}"
    email_text = (
        f"User '{user}' has committed code as author '{git_author_name}' to "
        f"active branch '{branch}' of '{GBT_CONFIG_PATH}' on {NOW}.\n\n"
        f"{proc_file_reminder}"
        "Commit info:\n"
        f"{'-'*80}\n{commit_log}\n{'='*80}\n\n"
        "Current status:\n"
        f"{'-'*80}\n {status}\n{'='*80}\n\n"
        "Changes in the latest commit:\n"
        f"{'-'*80}\n{changes_since_last_commit}\n{'='*80}"
    )

    email(subject=subject, text=email_text)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        hook_name = "post-commit"
        email(
            subject=f"GBT Config Warden: error in commit hook {hook_name}",
            text=f"{hook_name} failed with the following error:\n\n{traceback.format_exc()}",
        )
        raise ValueError("Hook failed! THIS DOES NOT AFFECT THE COMMIT") from error
