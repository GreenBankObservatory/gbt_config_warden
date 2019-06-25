"""Notify SDD after files are committed to GBT config repo"""

from hook_utils import (
    email,
    GBT_CONFIG_PATH,
    derive_git_author,
    derive_branch,
    derive_user,
    check_output,
    NOW,
)


def main():
    """CLI Main"""

    branch = derive_branch()
    git_author_name = derive_git_author()
    user = derive_user()

    diff = check_output(["git", "diff", "HEAD~"])
    commit = check_output(["git", "log", "HEAD^..HEAD"])
    status = check_output(["git", "status", "--untracked-files=no", "--short"])
    status = check_output(["git", "status", "--untracked-files=no", "--short"])
    files_in_last_commit = check_output(["git", "diff", "--name-only", "HEAD~"])

    proc_files_changed = [
        f"  * {line}"
        for line in files_in_last_commit.split("\n")
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

    subject = (
        f"GBT Config Warden: User '{user}' has committed files to {GBT_CONFIG_PATH}"
    )
    email_text = (
        f"User '{user}' has committed code as author '{git_author_name}' to "
        f"active branch '{branch}' of '{GBT_CONFIG_PATH}' on {NOW}.\n\n"
        f"{proc_file_reminder}"
        "Commit info:\n"
        f"{'-'*80}\n{commit}\n{'='*80}\n\n"
        "Current status:\n"
        f"{'-'*80}\n {status}\n{'='*80}\n\n"
        "Changes in the latest commit:\n"
        f"{'-'*80}\n{diff}\n{'='*80}"
    )

    email(subject=subject, text=email_text)


if __name__ == "__main__":
    main()
