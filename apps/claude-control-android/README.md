# Claude Control for Android

<img src="logo.png" width="96" align="right" alt="">

Claude Control on an Android phone: your sessions, usage notification and widgets, approvals, and Claude Control in
Android Auto. One app. (It was "CC Companion" until 1.0.0, and installs over it, keeping its link and settings.)

| | |
|---|---|
| Platform | Android 10+ |
| Releases | tag `claude-control-android-v<version>`, file `ClaudeControlAndroid-<version>.apk` |
| What's new | [CHANGELOG.json](CHANGELOG.json) |
| For the app's updater | [latest.json](latest.json) (`https://raw.githubusercontent.com/neil-bh/app-releases/main/apps/claude-control-android/latest.json`) |

<!-- latest:start (tools/publish writes this line) -->
<!-- latest:end -->

**Install:** on the Android phone, download the `.apk` from the latest release and open it (allow your browser to
install apps when Android asks). Then open Claude Control on the phone and use *Set up the app* to link it to Claude
Control on the Dell.

**Updates:** Settings › *Get the update* in the app reads `latest.json` here, downloads the APK, checks its SHA-256 and
hands it to Android's installer (Android asks you to confirm). When GitHub cannot be reached it falls back to Claude
Control on the Dell. Older copies of the app read the `cc-companion` feed, which every release here also updates.

Built apps only: the source is private. Check a download against the SHA-256 above (PowerShell:
`Get-FileHash <file>`; Linux: `sha256sum <file>`).
