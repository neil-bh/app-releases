# Claude Control for Windows

<img src="logo.png" width="96" align="right" alt="">

The Claude Control board in a window of its own, with your Claude usage in the Windows notification area.

| | |
|---|---|
| Platform | Windows 10/11 (64-bit) |
| Releases | tag `claude-control-windows-v<version>`, file `ClaudeControl-<version>.exe` |
| What's new | [CHANGELOG.json](CHANGELOG.json) |
| For the app's updater | [latest.json](latest.json) (`https://raw.githubusercontent.com/neil-bh/app-releases/main/apps/claude-control-windows/latest.json`) |

<!-- latest:start (tools/publish writes this line) -->
**Latest:** [Claude Control for Windows 1.7.5](https://github.com/neil-bh/app-releases/releases/download/claude-control-windows-v1.7.5/ClaudeControl-1.7.5.exe) (2026-11-24, 13.4 MB, SHA-256 `f15a124c5f1616c309a4eccd5edbd32b0ec5724d85ea7174d783fe04d10bcd98`) · [all releases](https://github.com/neil-bh/app-releases/releases?q=claude-control-windows&expanded=true)
<!-- latest:end -->

**Install:** download the `.exe` from the latest release and run it once: it installs itself for your Windows user
(no administrator needed), adds a Start menu entry and can start with Windows. It is not code-signed, so Windows may
warn that it is unrecognised: **More info › Run anyway**. It needs Tailscale signed in as the board's owner to reach the board.

**Updates:** the app checks on start, every few hours and from the tray's *Check for updates*. It reads
`latest.json` here, downloads the release asset, and installs it only when its size and SHA-256 match; when GitHub
cannot be reached it asks the board on the Dell instead.

Built apps only: the source is private. Check a download against the SHA-256 above (PowerShell:
`Get-FileHash <file>`; Linux: `sha256sum <file>`).
