# GBT Config Warden

The GBT is represented in software by the Monitor and Control System (M&C). The identify of the M&C System at a given time is comprised essentially of two parts:
1. The various executable files compiled from a given version of `ygor`/`gb`/`gbt`
2. The various configuration files from which these executables derive much of their state/behavior

Historically, there has been no explicit management of either of these sets of files. This repository represents an effort to change that: use git to track the state of both sets of files over time. We'll call each of these repositories a "Warded Repo". We have two basic goals:

1. Prevent "bad" changes from being made in the first place
2. Notify us when changes (of any kind) are made

These goals are each implemented by two mechanisms (with some overlap in responsibility):

1. Git Hooks: Prevent commits that violate policy; notify when checkouts are made
2. Config Warden: Periodically check a Warded Repo for locally modified files, and notify if there are any

## Policy

- Git Commits
    1. Only SDD members may commit to non-primary branch (where "the release branch" will be one of `19.4`, `22.1`, etc.)
    2. Commits may not be made as `monctrl` user (group accounts shield identity of the committer)
- File Changes
    1. SDD will be notified of "local modifications" to Warded files
    2. Notifications will continue until all local modifications are resolved (committed, deleted, etc.)

## Implementation

### Git Hooks

#### Prevent Unauthorized Changes (`pre_commit`)

A Warded Repo contains a `pre_commit` hook that checks the commit for any policy violations, and rejects it if there are any.

See `hooks/pre_commit.py` for implementation.

#### Notify When Branch Changes (`post_checkout`)

A Warded Repo contains a `post_checkout` hook that notifies SDD of every checkout that occurs. This is _typically_ the result of the `switchVersions` script, but not always. Regardless, we want to be kept apprised of this.

See `hooks/post_checkout.py` for implementation.



### File Changes (`repo_warden`)

A Repo Warden is a simple tool, intended to be run as a cron job, for checking on the status of the GBT config repository. If there are files that have been modified but not committed, this will be reported via email to RECIPIENT(S). If the repo is clean, only a debug email will go out via the cron daemon.

```cron
8 6 * * * /home/gbt1/gbt_config_warden/gbt_config_warden /home/gbt/etc/config <recipients>
8 6 * * * /home/gbt1/gbt_config_warden/gbt_config_warden /home/sim/etc/config <recipients>
8 6 * * * /home/gbt1/gbt_config_warden/gbt_release_warden /home/gbtversions/22.1 <recipients>
8 6 * * * /home/gbt1/gbt_config_warden/gbt_release_warden /home/simversions/22.1 <recipients>
```

Note that `gbt_config_warden` and `gbt_release_warden` are very thin wrappers around `repo_warden`; all they do is set `REPORT_NAME`, then call `repo_warden`


## Testing Notes

Testing notes:

1. Don't test in the production repo. Do a `$ cp -a` of the production GBT config and test there

2. Change `gbtconfig.debug = true` via `git config -e`. This will prevent emails from being sent (don't worry; they'll be printed to `stdout` instead)

3. Make changes

4. Verify the following use cases prior to making changes here:
    * As a whitelisted/non-blacklisted user:
        * On release branch:
            * Attempt commit (this should succeed): `git commit --allow-empty -m "test commit"`
            * Attempt commit as blacklist author (this should succeed): `git commit --allow-empty -m "test commit" --author=<blacklist-author>`
            * Attempt commit as non-blacklist author (this should fail): `git commit --allow-empty -m "test commit" --author=<non-blacklist-author>`
        * On non-release branch:
            * Attempt commit (this should succeed): `git commit --allow-empty -m "test commit"`
            * Attempt commit as blacklist author (this should succeed): `git commit --allow-empty -m "test commit" --author=<blacklist-author>`
            * Attempt commit as non-blacklist author (this should fail): `git commit --allow-empty -m "test commit" --author=<non-blacklist-author>`
    * As non-whitelisted/non-blacklisted user:
        * On release branch:
            * Attempt commit (this should succeed): `git commit --allow-empty -m "test commit"`
            * Attempt commit as blacklist author (this should succeed): `git commit --allow-empty -m "test commit" --author=<blacklist-author>`
            * Attempt commit as non-blacklist author (this should fail): `git commit --allow-empty -m "test commit" --author=<non-blacklist-author>`
        * On non-release branch:
            * Attempt commit (this should **fail**): `git commit --allow-empty -m "test commit"`
            * Attempt commit as blacklist author (this should **fail**): `git commit --allow-empty -m "test commit" --author=<blacklist-author>`
            * Attempt commit as non-blacklist author (this should **fail**): `git commit --allow-empty -m "test commit" --author=<non-blacklist-author>`
