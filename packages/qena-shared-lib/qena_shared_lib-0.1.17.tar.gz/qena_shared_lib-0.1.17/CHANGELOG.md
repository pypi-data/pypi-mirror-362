# Changelog

## [0.1.17] - 2025-07-16

### Changed

- Added `all` extra dependecies


## [0.1.16] - 2025-07-15

### Changed

- Added a prefix for environment variables with `QENA_SHARED_LIB_{MODULE_NAME}`
- Added optional extra dependencies


## [0.1.15] - 2025-06-28

### Changed

- Removed logger level set by dafault


## [0.1.14] - 2025-06-16

### Changed

- Remove unused generics variables
- Remove requirements.txt


## [0.1.13] - 2025-06-16

### Added

- Added pytest as one of pre-commit steps.
- Made http and rabbitmq exception handlers class based.
- Gracefull shutdown for rabbitmq and scheduler.

### Changed

- Moved logstash to remotelogging to generalize other forms of logging.
- Added loop class attribute for async event loop mixin.
- Made mypy type check slightly more strict.


## [0.1.12] - 2025-04-05

### Added

- Added a re-export for rabbitmq channel pool (ChannelPool) class.


[0.1.17]: https://github.com/Qena-Digital-Lending/qena-shared-kernel/compare/v0.1.16...v0.1.17
[0.1.16]: https://github.com/Qena-Digital-Lending/qena-shared-kernel/compare/v0.1.15...v0.1.16
[0.1.15]: https://github.com/Qena-Digital-Lending/qena-shared-kernel/compare/v0.1.14...v0.1.15
[0.1.14]: https://github.com/Qena-Digital-Lending/qena-shared-kernel/compare/v0.1.13...v0.1.14
[0.1.13]: https://github.com/Qena-Digital-Lending/qena-shared-kernel/compare/v0.1.12...v0.1.13
[0.1.12]: https://github.com/Qena-Digital-Lending/qena-shared-kernel/compare/v0.1.11...v0.1.12
