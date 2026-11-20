# Family Game Night

<img src="logo.png" width="96" align="right" alt="">

A party phrase game for the family: test builds for Android.

| | |
|---|---|
| Platform | Android (arm64) |
| Releases | tag `family-game-night-v<build>`, file `FamilyGameNight-<build>.apk` |
| What's new | [CHANGELOG.json](CHANGELOG.json) |
| For the app's updater | [latest.json](latest.json) (`https://raw.githubusercontent.com/neil-bh/app-releases/main/apps/family-game-night/latest.json`) |

<!-- latest:start (tools/publish writes this line) -->
**Latest:** [Family Game Night 465260](https://github.com/neil-bh/app-releases/releases/download/family-game-night-v465260/FamilyGameNight-465260.apk) (2026-11-20, 25.7 MB, SHA-256 `036704e05ff69d9acf32aabb2d355efc958db5adaa76f82a4b51c75da2c84491`) · [all releases](https://github.com/neil-bh/app-releases/releases?q=family-game-night&expanded=true)
<!-- latest:end -->

**Install:** on an Android phone, download the `.apk` from the latest release and open it.

**Updates:** the game reads `latest.json` here on start and offers *Update now*, after checking the download's size and
SHA-256. Its build number is minutes since 2026-01-01 UTC, so it always increases. Releases are published by its own
`scripts/release_apk.sh`, which uses `tools/publish`.

Built apps only: the source is private. Check a download against the SHA-256 above (PowerShell:
`Get-FileHash <file>`; Linux: `sha256sum <file>`).
