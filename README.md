# GBT Config Warden

## gbt_config_warden

### Usage

`$ gbt_config_warden REPO_PATH [RECIPIENT ...]`

A simple tool, intended to be run as a cron job, for checking on the status of the GBT config repository. If there are files that have been modified but not committed, this will be reported via email to RECIPIENT(S). If the repo is clean, only a debug email will go out via the cron daemon.


## Hooks

### Testing Notes

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
