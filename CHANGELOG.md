# Changelog
## [0.3.0-dev0] - 19-02-18
### Changed
* todo

## [0.2.1-rc0] - 19-02-11
### Added
+ csemver now supports adding versions `csemver.parse("a.b.c") + csemver.parse("d.e.f")`
+ parse method added as a shortcut for `csemver.csemver(version)`
+ prerelease and build fields to set prerelease and build-tag
+ Introduced python2 support (maybe it will be dropped in the future)
+ Added unit tests
+ Added index operator to object, it is now possible to select specific parts with
  with `a['major'], a['minor'], a['patch'], a['prerelease'], a['build']`. The fields are also writeable.

### Fixed
* `csmver.parse` does not had a default value
* some getters did not return a value

### Changed
* `incMajor, incMinor, incPatch` are now chainable and support additional integer parameter to specify amount
* Added deprecation warning to setNumber
* `a.number` will return an string instead of an dict.

## [0.1.0] - 19-02-10
### Added
+ csemver class
+ Docstrings for `number`,`incMajor, incMinor, incPatch`

[0.2.1-rc0]: https://github.com/sebi2020/csemver/compare/v0.1.0...v0.2.1-rc0
[0.1.0]: https://github.com/sebi2020/csemver/compare/20f2f6f0810937af5fbc8f1ce7fc3d4a2383b28b...v0.1.0