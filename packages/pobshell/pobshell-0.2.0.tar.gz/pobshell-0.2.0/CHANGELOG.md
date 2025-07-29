# Changelog

All notable changes to this project will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com).

## [0.2.0] - 2025-07-15
### Added
- Add negative filters: `--nmodule PATTERN`  and `--nismodule` 
- Add `--nstr PATTERN` filter
### Changed
- Rename `--nfile` as `--nfilepath` for consistency
- Remove `--value PATTERN` and `--nvalue PATTERN` filters

## [0.1.4] - 2025-07-01
### Changed
- Minimum supported Python lowered from 3.12 to 3.11
### Internal
- Add .yml spec for Py 3.11 test environment
- Rename prior .yml specs to be consistent
- Add & rename test transcripts to match

## [0.1.3] - 2025-06-24
### Changed
- Fix terminal width detection bug
- Change idiosyncratic Welcome banner

## [0.1.2] - 2025-06-22
### Added
- New `flatten_multiline` setting (default: `False`)
  - Forces multiline command output to a single line
  - Useful with `str` or `repr` when piping to `sort`, `uniq`, or `wc -l`
- man command now accepts `-p` option to view output in pager
- Additional man pages were added
### Changed
- `-q` option also removes blank separator lines between multiline outputs
  - Updated transcript test to reflect new -q behaviour  
- `man` with no topic now shows an intro to man pages
- Updated man pages to reflect recent commands and filters
- Change default 'find' command trace_frequency to 500 when DEBUG is False
- Changed Pobshell Welcome banner
- Changed 'help -v' and 'help' header, to mention 'man' command

## [0.1.1] - 2025-06-20
### Changed
- `Pobshell` now defaults to `Pobprefs.DEBUG = False` instead of `DEBUG = True`
- `DEBUG` is now an optional keyword argument to pobshell.shell() and .pob()
### Internal
- Test file paths updated to use more generic environment names

## [0.1.0] - 2025-06-19
### Added
- Initial release of Pobshell
- Core commands: ls, cat, doc, tree, find, memsize, etc.
- Bash-style navigation for Python objects
- Filter system (`--isfunction`, `--doc PATTERN`, etc.)
- OS shell integration with pipes and `!` commands
- `map` modes: attributes, contents, everything, static,...
- Alpha-level safety precautions

