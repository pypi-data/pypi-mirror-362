# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-07-16 (Release)

### Added | 2025-07-16 16:09:24

- Add support for 'version' command and improve existing CLI and version info handling

- Introduces a new `version` command in the CLI to display detailed version and environment info, including package version, Python version, platform, system, architecture, installation path, and documentation URL.

- Enhances the `cli.py` module with improved type annotations, clearer function signatures, and refined logging.

- Updates `utils.py` to better handle version retrieval, including fallback to `pyproject.toml` with debug print statements.

- Modifies `config.py` to improve validation messages for base DN and auto-detect options.

- Adds a new "Version Information" table display for comprehensive environment details.

- Refactors related test cases to ensure coverage and correctness

## [1.0.0] - 2025-07-16 (Release)

### Added | 2025-07-16 16:09:21

- added version command

## [0.1.0-alpha.26] - 2025-06-26 (Alpha)

### Added | 2025-06-26 12:15:50

- Fix base DN validation and add PowerShell module auto-install

### Files Changed (1) | 2025-06-26 12:15:50

- Modified: tests/test_models.py

## [0.1.0-alpha.25] - 2025-06-26 (Alpha)

### Fixed | 2025-06-26 11:42:07

- fixed issue with base_dn being required when its not

### Files Changed (3) | 2025-06-26 11:42:07

- Modified: ad_user_manager/config.py
- Modified: ad_user_manager/powershell_manager.py
- Modified: tests/test_models.py

## [0.1.0-alpha.24] - 2025-06-26 (Alpha)

### Fixed | 2025-06-26 11:05:22

- fixed issue with get_version when installed as a package

### Files Changed (1) | 2025-06-26 11:05:22

- Modified: ad_user_manager/utils.py

## [0.1.0-alpha.23] - 2025-06-26 (Alpha)

### Fixed | 2025-06-26 11:02:05

- fixed issue with get_version when installed as a package

### Files Changed (1) | 2025-06-26 11:02:05

- Modified: ad_user_manager/utils.py

## [0.1.0-alpha.22] - 2025-06-26 (Alpha)

### Added | 2025-06-26 10:52:21

- add get_version_info as a function

## [0.1.0-alpha.21] - 2025-06-26 (Alpha)

### Added | 2025-06-26 10:28:06

- add get_version_info as a function

### Files Changed (2) | 2025-06-26 10:28:06

- Modified: example_usage.py
- Modified: pyproject.toml

## [0.1.0-alpha.20] - 2025-06-26 (Alpha)

### Added | 2025-06-26 09:33:43

- add get_version_info as a function

### Files Changed (1) | 2025-06-26 09:33:43

- Modified: pyproject.toml

## [0.1.0-alpha.19] - 2025-06-26 (Alpha)

### Added | 2025-06-26 09:20:08

- add get_version_info as a function

### Files Changed (3) | 2025-06-26 09:20:08

- Modified: ad_user_manager/cli.py
- Modified: example_usage.py
- Modified: pyproject.toml

## [0.1.0-alpha.18] - 2025-06-26 (Alpha)

### Added | 2025-06-26 08:59:10

- add get_version_info as a function

### Files Changed (5) | 2025-06-26 08:59:10

- Modified: ad_user_manager/**init**.py
- Modified: ad_user_manager/cli.py
- Modified: ad_user_manager/utils.py
- Modified: example_usage.py
- Modified: pyproject.toml

## [0.1.0-alpha.17] - 2025-06-26 (Alpha)

### Fixed | 2025-06-26 08:36:13

- Fix DCServerConfig base_dn validation error for auto-detection support

## [0.1.0-alpha.16] - 2025-06-25 (Alpha)

### Added | 2025-06-25 16:44:50

- fix upload to github workflow portion and add local ci script

### Files Changed (2) | 2025-06-25 16:44:50

- Modified: .github/workflows/pypi-publish.yml
- Modified: pyproject.toml

## [0.1.0-alpha.15] - 2025-06-25 (Alpha)

### Added | 2025-06-25 16:42:34

- fix upload to github workflow portion and add local ci script

### Files Changed (3) | 2025-06-25 16:42:34

- Modified: .github/workflows/pypi-publish.yml
- Modified: pyproject.toml
- Untracked: python-ci-plan.md

## [0.1.0-alpha.14] - 2025-06-25 (Alpha)

### Added | 2025-06-25 16:36:06

- fix upload to github workflow portion and add local ci script

### Files Changed (5) | 2025-06-25 16:36:06

- Modified: .github/workflows/pypi-publish.yml
- Modified: .gitignore
- Modified: pyproject.toml
- Modified: scripts/local-ci.sh
- Untracked: scripts/README.md

## [0.1.0-alpha.13] - 2025-06-25 (Alpha)

### Fixed | 2025-06-25 16:33:51

- fix upload to github workflow portion

### Files Changed (3) | 2025-06-25 16:33:51

- Modified: .github/workflows/pypi-publish.yml
- Modified: pyproject.toml
- Untracked: scripts/local-ci.sh

## [0.1.0-alpha.12] - 2025-06-25 (Alpha)

### CI | 2025-06-25 16:30:57

- making local ci clone

### Files Changed (1) | 2025-06-25 16:30:57

- Modified: pyproject.toml

## [0.1.0-alpha.11] - 2025-06-25 (Alpha)

### Changed | 2025-06-25 16:18:01

- update yml

## [0.1.0-alpha.10] - 2025-06-25 (Alpha)

### Changed | 2025-06-25 16:09:47

- update yml

### Files Changed (1) | 2025-06-25 16:09:47

- Modified: .github/workflows/code-quality.yml

## [0.1.0-alpha.10] - 2025-06-25 (Alpha)

### Test | 2025-06-25 16:07:08

- tests: 133 passed in 0.34s

### Files Changed (2) | 2025-06-25 16:07:08

- Modified: pyproject.toml
- Modified: tests/test_validators.py

## [0.1.0-alpha.9] - 2025-06-25 (Alpha)

### Changed | 2025-06-25 16:05:08

- reformatted /Users/vincevasile/Documents/dev/python/mansol/ad_user_manager/ad-user-manager/tests/test_powershell_manager.py
  reformatted /Users/vincevasile/Documents/dev/python/mansol/ad_user_manager/ad-user-manager/tests/test_ldap_manager.py
  reformatted /Users/vincevasile/Documents/dev/python/mansol/ad_user_manager/ad-user-manager/tests/test_validators.py

All done! ✨ 🍰 ✨
3 files reformatted, 19 files left unchanged.

### Files Changed (4) | 2025-06-25 16:05:08

- Modified: pyproject.toml
- Modified: tests/test_ldap_manager.py
- Modified: tests/test_powershell_manager.py
- Modified: tests/test_validators.py

## [0.1.0-alpha.8] - 2025-06-25 (Alpha)

### Test | 2025-06-25 16:04:25

- tests: 133 passed in 0.34s

## [0.1.0-alpha.7] - 2025-06-25 (Alpha)

### Added | 2025-06-25 15:46:24

- adding tests/working through failures - fix workflows

### Files Changed (3) | 2025-06-25 15:46:24

- Modified: .github/workflows/code-quality.yml
- Modified: .github/workflows/python-ci.yml
- Modified: pyproject.toml

## [0.1.0-alpha.6] - 2025-06-25 (Alpha)

### Added | 2025-06-25 15:42:20

- adding tests/working through failures

## [0.1.0-alpha.5] - 2025-06-25 (Alpha)

### Removed | 2025-06-25 14:34:06

- remove broken test

### Files Changed (2) | 2025-06-25 14:34:06

- Modified: pyproject.toml
- Deleted: tests/test_powershell_manager.py

## [0.1.0-alpha.4] - 2025-06-25 (Alpha)

### Added | 2025-06-25 14:31:30

- added workflow files

### Files Changed (4) | 2025-06-25 14:31:30

- Modified: pyproject.toml
- Untracked: .github/workflows/code-quality.yml
- Untracked: .github/workflows/pypi-publish.yml
- Untracked: .github/workflows/python-ci.yml

## [0.1.0-alpha.3] - 2025-06-25 (Alpha)

### Changed | 2025-06-25 11:44:22

- cleanup gitignore

## [0.1.0-alpha.2] - 2025-06-25 (Alpha)

### Added | 2025-06-25 11:43:22

- initial push for ad-user-manager, an interactive python module to create ad users with powershell or ldap, defaulting to powershell, this is meant to be used as a bot in asio

## [0.1.0-alpha.2] - 2025-06-25 (Alpha)

### Added | 2025-06-25 11:28:05

- initial push for ad-user-manager, an interactive python module to create ad users with powershell or ldap, defaulting to powershell, this is meant to be used as a bot in asio

### Files Changed (1) | 2025-06-25 11:28:05

- Untracked: .git_simplifier_backups/backup_20250625_112804.json

## [0.1.0-alpha.2] - 2025-06-25 (Alpha)

### Added | 2025-06-25 11:24:59

- initial push for ad-user-manager, an interactive python module to create ad users with powershell or ldap, defaulting to powershell, this is meant to be used as a bot in asio
