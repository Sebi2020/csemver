# Changelog

## [Unreleased]
### Added
+ csemver now supports adding versions `csemver.parse("a.b.c") + csemver.parse("d.e.f")`
+ parse method added as a shortcut for `csemver.csemver(version)`
+ prerelease and build fields to set prerelease and build-tag
+ Introduced python2 support (maybe it will be dropped in the future)
+ Added unit tests

### Changed
* `incMajor, incMinor, incPatch` are now chainable and support additional integer parameter to specify amount
* Added deprecation warning to setNumber

## [0.1.0] - 19-02-10
### Added
+ csemver class
+ Docstrings for `number`,`incMajor, incMinor, incPatch`

[0.2.0]: https://github.com/sebi2020/csemver/compare/20f2f6f0810937af5fbc8f1ce7fc3d4a2383b28b...v0.2.0

