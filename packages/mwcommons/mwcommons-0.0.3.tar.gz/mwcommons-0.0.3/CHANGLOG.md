# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Best Practices
Update the Changelog for Each Release:
- Make updates part of your release process.
- Group Changes by Type: Common categories include:
  - Added: New features.
  - Changed: Changes to existing functionality.
  - Deprecated: Features that will be removed in future versions.
  - Removed: Features that are no longer available.
  - Fixed: Bug fixes.
  - Security: Notable security improvements or fixes.

How can I reduce the effort required to maintain a changelog?
 - Keep an Unreleased section at the top to track upcoming changes.
  - This serves two purposes:
    - People can see what changes they might expect in upcoming releases
    - At release time, you can move the Unreleased section changes into a new release version section.

## [Unreleased] - 2025-01-10
### Added
- The changelog file.
- Update the readme file.
### Changed
- The project name is now mw-utils.
- Project dependencies manager is no uv.
### Fixed 
- Expose the logger handler to the user.
- Prevents bad use of severity_level in GeneralException.

## [0.0.1] - 2024-11-27
### Added
- Exceptions handling.
- Default types for schemas using ticdat.
- Utility methods for ticdat.
- Logging formatter based on the level of the message.

