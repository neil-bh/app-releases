# Family Game Night

A party phrase game for the family: test builds for Android.

| | |
|---|---|
| Platform | Android (arm64) |
| Releases | tag `family-game-night-b<version>`, file `family-game-night-b<version>.apk` |
| What's new | [CHANGELOG.json](CHANGELOG.json) |
| For the app's updater | [latest.json](latest.json) (`https://raw.githubusercontent.com/neil-bh/app-releases/main/apps/family-game-night/latest.json`) |

<!-- latest:start (tools/publish writes this line) -->
**Latest:** [Family Game Night 454186](https://github.com/neil-bh/app-releases/releases/download/family-game-night-b454186/family-game-night-b454186.apk) (2026-11-12, 25.6 MB, SHA-256 `b36ef364bafc9d4a060c7637662c6cc4cd267db05fb600c923df74ae2076df5e`) · [all releases](https://github.com/neil-bh/app-releases/releases?q=family-game-night&expanded=true)
<!-- latest:end -->

**Install:** on an Android phone, download the `.apk` from the latest release and open it.

**Updates:** the game checks this repo's releases on start (tag prefix `family-game-night-b`, ADR-0015 in its own
project) and offers *Update now*. Its build number is minutes since 2026-01-01 UTC, so it always increases. Its
releases are published by its own `scripts/release_apk.sh`, not `tools/publish`.

Built apps only: the source is private. Check a download against the SHA-256 above (PowerShell:
`Get-FileHash <file>`; Linux: `sha256sum <file>`).
