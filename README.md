# GBT Config Warden

Usage:
`$ gbt_config_warden REPO_PATH [RECIPIENT ...]`

A simple tool, intended to be run as a cron job, for checking on the status of the GBT config repository. If there are files that have been modified but not committed, this will be reported via email to RECIPIENT(S). If the repo is clean, only a debug email will go out via the cron daemon.
