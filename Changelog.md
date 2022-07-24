# Changelog

A plugin for [Touch Portal](https://www.touch-portal.com/) to have information about Twitch streamers

Here there is going to be the changelog of the new versions of the plugin

## [Released]

## [1.0.0] - 2022.07.09 | Release

All of the basic features on the plugin

## [1.0.1] - 2022.07.11 | Minor fixes

### Added

- Refresh button example in [helpers](./helpers/touchportal/buttons)

### Changed

- Sdk version change from 3 to 6 to group `refresh_state` and `time_until_refresh` states under the name of `Twitch Activity` throughout Touch Portal menus

- Default value for `Dynamic image (bool)` from false (0) to true (1)
- To avoid problem and misunderstandings any patch is going to add a version to the plugin, so now it's on version 2 🎉

### Fixed

- Logging event exposing `CLIENT-SECRET` and `CLIENT-ID` of Twitch API now removed
- On the showcase page, the refresh button was colored red every time it was updated instead of green

## [1.0.2] - 2022.07.12 | Less crashes

### Added

- When entering the list in `Channel Names` it now automatically removes spaces to avoid errors or missing data

### Fixed

- Data in title of previous version now is the correct one
- API requests should now no longer crash the plugin

## [1.0.3] - 2022.07.14 | Visual improvement and fixed start crash

### Added
- When the settings are updating the counter is set to `x`
- Added a blank icon to help TP to 'refresh' the visual 

### Fixed
- On startup, if offline, the plugin should no longer crash and will set up channels once it is online
- In the helpers the icon didn't update because the default one wasn't nothing and it covered the plug-in icon being on a higher level


<!-- ## [Unreleased] -->
<!--
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security -->

[released]: https://github.com/JustCoderdev/TwitchActivity/releases

<!-- [unreleased]: https://github.com/JustCoderdev/TwitchActivity -->

[1.0.0]: https://github.com/JustCoderdev/TwitchActivity/tree/d5b02548cd3f141b0994c05cfed2e136c222fb90
[1.0.1]: https://github.com/JustCoderdev/TwitchActivity/tree/d4de7b5ebb64ea9d45755294f22e8d6bb2cf3b4a
[1.0.2]: https://github.com/JustCoderdev/TwitchActivity/tree/63585f733113ce215415e845e96538d5620764fa
[1.0.3]: https://github.com/JustCoderdev/TwitchActivity/tree/
