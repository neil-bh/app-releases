# CC Companion

<img src="logo.png" width="96" align="right" alt="">

Claude Control Companion: usage notification and widgets on an Android phone, and Claude Control in Android Auto.

| | |
|---|---|
| Platform | Android 10+ |
| Releases | tag `cc-companion-v<version>`, file `ClaudeControlCompanion-<version>.apk` |
| What's new | [CHANGELOG.json](CHANGELOG.json) |
| For the app's updater | [latest.json](latest.json) (`https://raw.githubusercontent.com/neil-bh/app-releases/main/apps/cc-companion/latest.json`) |

<!-- latest:start (tools/publish writes this line) -->
**Latest:** [CC Companion 1.3.3](https://github.com/neil-bh/app-releases/releases/download/cc-companion-v1.3.3/ClaudeControlCompanion-1.3.3.apk) (2026-11-20, 11.8 MB, SHA-256 `52214086cd5875664b3e96ed245583a1c1eceb4c25513f1923527b7e27aa3d7a`) · [all releases](https://github.com/neil-bh/app-releases/releases?q=cc-companion&expanded=true)
<!-- latest:end -->

**Install:** on the Android phone, download the `.apk` from the latest release and open it (allow your browser to
install apps when Android asks). Then open Claude Control on the phone and use *Set up the app* to link it to your board.

**Updates:** Settings › *Get the update* in the app reads `latest.json` here, downloads the APK, checks its SHA-256 and
hands it to Android's installer (Android asks you to confirm). When GitHub cannot be reached it falls back to the board.

Built apps only: the source is private. Check a download against the SHA-256 above (PowerShell:
`Get-FileHash <file>`; Linux: `sha256sum <file>`).
