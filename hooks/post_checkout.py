"""Notify SDD after checkout is performed in GBT config repo"""

import argparse
import sys
import traceback

from hook_utils import (
    check_output,
    DEBUG,
    derive_branch,
    derive_git_author,
    derive_user,
    email,
    GBT_CONFIG_PATH,
    get_changed_filenames,
    get_proc_file_reminder,
    get_ref_name,
    get_status,
    NOW,
)


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="See: https://git-scm.com/docs/githooks#_post_checkout",
    )
    parser.add_argument("prev_ref", help="the ref of the previous HEAD")
    parser.add_argument(
        "new_head", help="the ref of the new HEAD (which may or may not have changed)"
    )
    parser.add_argument(
        "flag",
        help="flag indicating whether the checkout was a branch checkout "
        "(changing branches, flag=1) or a file checkout (retrieving a file from the index, flag=0)",
    )
    return parser.parse_args()


def main():
    """CLI Main"""

    args = parse_args()
    if DEBUG:
        print(f"Got args: {args}")

    git_author_name = derive_git_author()
    user = derive_user()

    status = get_status()

    proc_file_reminder = get_proc_file_reminder(get_changed_filenames(args.prev_ref, args.new_head))

    prev_ref_name = get_ref_name(args.prev_ref)
    new_head_name = get_ref_name(args.new_head)

    subject = (
        f"GBT Config Warden: Author '{git_author_name}' has changed branch "
        f"from {prev_ref_name!r} to {new_head_name!r} in {GBT_CONFIG_PATH}"
    )
    email_text = (
        f"User '{user}' (author '{git_author_name}') has performed a checkout in "
        f"{GBT_CONFIG_PATH!r} from {prev_ref_name!r} to "
        f"{new_head_name!r} at {NOW}.\n\n"
        f"{proc_file_reminder}"
        "Current status:\n"
        f"{'-'*80}\n {status}\n"
    )

    email(subject=subject, text=email_text)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        hook_name = "post-checkout"
        email(
            subject=f"GBT Config Warden: error in commit hook {hook_name}",
            text=f"{hook_name} failed with the following error:\n\n{traceback.format_exc()}",
        )
        raise ValueError("Hook failed! THIS DOES NOT AFFECT THE CHECKOUT") from error
