# 0.7.4 - In Development

*TBD*

# 0.7.3 - September 29th, 2024

- Dependencies update
- Re-added Nuika support (after upstream fixed it)
- Removed pre-commit dependency

# 0.7.2 - August 8th, 2024

- Python 3.12 support
- Dependencies update
- Better handling of weird builddir states.
- Clear warning in Nuitka regarding pkgutils use
- Fix utils.hashfile
- Added `original_file` parameter to `buildtools.maestro.web.CacheBashifyFiles.__init__()`
- Added `original_file` attribute to `buildtools.maestro.web.CacheBashifyFiles`
- Renamed `source` parameter to `source_file` in `buildtools.maestro.web.CacheBashifyFiles.__init__()`

# 0.7.1 - February 14th, 2024

- Changed back to `subprocess.run` for internal process calls due to instability on Windows

# 0.7.0 - February 14th, 2024

- **BREAKING CHANGES:**
  - Nuitka:
    - Re-introduced NuitkaTarget.getCommandLine()
    - Changed to `subprocess_tee.run` for internal process calls
    - Added some flags for disabling output
    - Better error handling
- Dependency update

# 0.6.2

- lxml update

# 0.6.2 - January 6th, 2024

- Fixed: `BuildEnv.clone()` always returns `None`.

# 0.6.1 - January 5th, 2024

- Added: sudo support to git repo and git wrapper.

# 0.6.0 - December 29th, 2023

- **BREAKING CHANGES:**
  - `pybuildtools.pygit2_callbacks.RemoteProgressCallbacks` => `pybuildtools.pygit2_callbacks.TQDMRemoteProgressCallbacks`
- Added `pybuildtools.pygit2_callbacks.RichRemoteProgressCallbacks`
- Fixed: Dumb typo in nuitka_plus.
- Fixed: Dep conflicts due to lxml weirdness.

# 0.5.14 - July 4th, 2023

- Fixed: Nuitka throwing errors because it cannot find patchelf on Linux.

# 0.5.13 - July 2nd, 2023

- Added: Option to make NuitkaBuildTarget use CLI launch, in case nuitka_plus experiences an unfortunate implosion.

# 0.5.12 - June 18th, 2023

- Fixed: Crash in `coctweak.utils.hashfile` because .pyi files lie
- Fixed: Crashes in `coctweak.os_utils.Chdir` caused by concatenating a PosixPath and a string

# 0.5.11 - June 18th, 2023

- **BREAKING:** buildtools.os_utils.SCRIPTS_DIR moved to buildtools.paths
- **BREAKING:** buildtools.os_utils.BUILDTOOLS_DIR moved to buildtools.paths
- Clean-up and typing fixage
- Dependency changes

# 0.5.10 - May 4th, 2023

- Fixed: More cache issues.

# 0.5.9 - May 4th, 2023

- Added: `NuitkaBuildTarget.copyright` to set `--copyright`
- Added: `NuitkaBuildTarget.other_opts` to set arbitrary command line arguments for forward compatibility.
- Added: Nuitka is wrapped in a small module that reads command line flags from a file, to get around Windows CLI limits.
- Fixed: http.DownloadFile not returning a bool
- Fixed: Maestro caches failing to serialize due to ruamel.yaml changes.

# 0.5.7 - April 19th, 2023

- **BREAKING:** Major Nuitka changes. Rewrite your packaging scripts!
- Dependency updates

# 0.5.6 - April 10th, 2023

- Nuitka now supports `--recurse-none`, `--recurse-to`, `--pgo`, `--lto=yes`, and `--python-flags`.
- Dependency updates

# 0.5.4 - October 24th, 2022

- Dependency updates
- pyproject.toml cleanup

# 0.5.1 - August 7th, 2022

- Crash fixes

# 0.5.0 - August 7th, 2022

- **BREAKING CHANGES:**
  - `buildtools.maestro.base_target.BaseTarget.genVirtualTarget()`:
    - Takes BuildMaestro as its first argument.
  - `buildtools.maestro.fileio.ReplaceTextTarget()`:
    - `subject` attribute renamed to `original_filename`
  - `buildtools.maestro.fileio.RSyncRemoteTarget()`:
    - Takes BuildMaestro as its first argument.
  - `buildtools.maestro.fileio.ExtractArchiveTarget()`:
    - Takes BuildMaestro as its first argument.
  - `buildtools.maestro.shell.CommandBuildTarget()`:
    - Takes BuildMaestro as its first argument.
  - `buildtools.maestro.web.CacheBashifyFiles()`:
    - Uses the generated manifest file as its target, rather than a virtual target.
- Maestro:
  - Many buildtargets now have type hinting and renamed args.

# 0.4.16 - June 29th, 2022

- Maestro:
  - Closed a hole for Path leaks into Maestro.
- More type-hinting improvements
- Added buildtools.consts
  - SysExits enum for common exit codes
  - LogPrefixes for common hax0r logging prefixes

# 0.4.14 - May 23rd, 2022

- Maestro:
  - Fixed `RonnBuildTarget`, which was using old CLI switches.
- Added "all" extra.

# 0.4.13 - May 23rd, 2022

- Maestro:
  - `BuildMaestro.{saveTo,loadFrom}Rules()` removed due to being broken and unused.
  - `BuildMaestro.generateVirtualTarget()` added for things like `CopyFilesTarget`
  - `GenEnumsTarget` largely rewritten to fix numerous issues.
  - Tracing of duplicate targets added
- Type hinting improved

# 0.4.12 - April 10th, 2022

- Fixed jinja2 Markup crash
- Nuitka buildtarget now correctly grabs getEnabledPlugins().
- `buildtools.cli` is now marked as deprecated, as `click` is _way_ better.
- `buildtools.as3` was cleaned up a bit.
- `buildtools.indentation` was also cleaned up, and a few methods renamed to use proper snakeCasing.
  - `GenIndentDeltas` => `genIndentDeltas`

# 0.4.11 - April 4th, 2022

- Nuitka BuildTarget now auto-detects which plugins are always active and removes them from the active set.
- Added `lazy_tqdm` and `ascii` options to pygit2 callbacks
- Twisted is now an optional dependency (pull by using the `twisted` extra)
- PyQt5 is now an optional dependency (pull by using the `pyqt5` extra)

# 0.4.10

- Fixed pygit2 callbacks

# 0.4.9 - March 12th, 2022

- Hotfix for Nuitka

# 0.4.5 - December 1st, 2021

- Hotfix for code generation

# 0.4.4 - December 1st, 2021

- Fixes to code generation
- Fixes to maestro

# 0.4.2 - January 16th, 2021

- More crash fixes.

# 0.4.1 - January 16th, 2021

- Fixed crash in config and salt.

# 0.4.0 - January 16th, 2021

- Removed PyYAML in favor of ruamel.yaml, which is YAML 1.2-compliant and updated more frequently.
- `os_utils._args2str()` now uses `shlex.quote` instead of a homebrew solution.
- Fix error regarding `__failed` attribute in some Maestro targets.

# 0.3.6 - July 13th, 2020

- Fix CopyFileTarget not accepting filename as target. **BREAKING CHANGE!**

# 0.3.5 - July 4th, 2020

- Fix lack of default values in maestro args.
- Fix crashes in Maestro.

# 0.3.4 - July 4th, 2020

- Fix Jinja2 rendering issues in BaseConfig.
- Fix default arguments to YAMLConfig being template_dir = `.`, which bugs out things that expect absolute pathing.

# 0.3.2 - June 19th, 2020

- Fix pathing issues with BaseConfig.

# 0.3.1 - June 19th, 2020

- Fixed debug spam in PipeReader

# 0.3.0 - June 11th, 2020

Python >=3.6 release. Change tracking begins.
