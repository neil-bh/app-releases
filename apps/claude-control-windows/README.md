# Claude Control for Windows

The Claude Control board in a window of its own, with your Claude usage in the Windows notification area.

| | |
|---|---|
| Platform | Windows 10/11 (64-bit) |
| Releases | tag `claude-control-windows-v<version>`, file `ClaudeControl-<version>.exe` |
| What's new | [CHANGELOG.json](CHANGELOG.json) |
| For the app's updater | [latest.json](latest.json) (`https://raw.githubusercontent.com/neil-bh/app-releases/main/apps/claude-control-windows/latest.json`) |

<!-- latest:start (tools/publish writes this line) -->
**Latest:** [Claude Control for Windows 1.3.2](https://github.com/neil-bh/app-releases/releases/download/claude-control-windows-v1.3.2/ClaudeControl-1.3.2.exe) (2026-11-19, 13.3 MB, SHA-256 `bb60e956c24bd0fbdcb3ef7ea931f69aa13cd486dbd9e756ccecc7bb10cc9fd6`) · [all releases](https://github.com/neil-bh/app-releases/releases?q=claude-control-windows&expanded=true)
<!-- latest:end -->

**Install:** download the `.exe` from the latest release and run it once: it installs itself for your Windows user
(no administrator needed), adds a Start menu entry and can start with Windows. It is not code-signed, so Windows may
warn that it is unrecognised: **More info › Run anyway**. It needs Tailscale signed in as the board's owner to reach the board.

**Updates:** the app checks on start, every few hours and from the tray's *Check for updates*. It reads
`latest.json` here, downloads the release asset, and installs it only when its size and SHA-256 match; when GitHub
cannot be reached it asks the board on the Dell instead.

Built apps only: the source is private. Check a download against the SHA-256 above (PowerShell:
`Get-FileHash <file>`; Linux: `sha256sum <file>`).
