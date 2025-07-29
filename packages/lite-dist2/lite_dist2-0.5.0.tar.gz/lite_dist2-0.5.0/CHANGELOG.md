# Changelog

## [0.5.0] - 2025-07-15

### Changed
- Changed the location of Trials from a single curriculum file to a file for each Trial([#21](https://github.com/atsuhiron/lite_dist2/pull/21)).
  - The smaller size of the curriculum file no longer causes problems with failed saves or timeout errors caused by too much time spent on saving.

### Fixed
- Fixed notation of time taken to save curriculum.json at a table node([#22](https://github.com/atsuhiron/lite_dist2/pull/22)).

## [0.4.0] - 2025-06-29

### Added
- Added /status/progress API. ([#19](https://github.com/atsuhiron/lite_dist2/pull/19))
  - This API can show ETA of studies.

## [0.3.1] - 2025-06-25

### Changed
- Changed schema of study storage ([#15](https://github.com/atsuhiron/lite_dist2/pull/15))
  - Rethinking the `result` schema, it reduced its size by roughly 1/4.

### Fixed
- Fixed count grid. Running trial is no longer accounted for as done ([#14](https://github.com/atsuhiron/lite_dist2/pull/14)).
- Fixed `TableNodeClient` so that processing continues without error when a timeout of `Trial` occurs ([#16](https://github.com/atsuhiron/lite_dist2/pull/16)).
- Fixed type hinting of README ([#17](https://github.com/atsuhiron/lite_dist2/pull/17))

## [0.3.0] - 2025-06-22

### Added
- Added `CostParam` to `Study`.
  - It is now possible to have constants in a Study that are not related to grid parameter space.

## [0.2.3] - 2025-06-21

### Fixed
- Fixed a bug that caused grid values to change slightly (rounding error) depending on the segment start position ([#10](https://github.com/atsuhiron/lite_dist2/pull/10)).

## [0.2.2] - 2025-06-18

### Fixed
- Fixed a bug that occurred when using multiple worker nodes ([#7](https://github.com/atsuhiron/lite_dist2/pull/7)).
- Bump up `ruff` version to 0.12.0. and fix some new warnings ([#8](https://github.com/atsuhiron/lite_dist2/pull/8)).

## [0.2.1] - 2025-06-14

### Fixed
- Fixed a bug that table threads were not terminated ([#4](https://github.com/atsuhiron/lite_dist2/pull/5)).

## [0.2.0] - 2025-06-14

### Added
- Added Worker node ID ([#2](https://github.com/atsuhiron/lite_dist2/pull/2))
  - When Trial registers, it will look at this ID and only accept results from the same node as the reserved node.
- Added DELETE /study API ([#3](https://github.com/atsuhiron/lite_dist2/pull/3))
- Added flag to automatically terminate the worker thread
  - Set a flag like `worker.start(stop_at_no_trial=True)` to automatically terminate the worker node when a Trial is not obtained.
- Added `.stop()` method to table node thread (getting `start_in_thread()` function)
- Added `.save()` method to `TableNodeClient`.

### Fixed
- Fixed type hinting of `*args` and `**kwargs`.
