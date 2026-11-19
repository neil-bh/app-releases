# app-releases

Public downloads for test builds of private projects. Built apps only (APKs, Windows programs and similar), never source code.

Each app has a folder, `apps/<app-id>/`, with its README (what it is, how to install and update it), its
`CHANGELOG.json` and, once something is published, `latest.json`, which the app itself reads to update. The files
are GitHub Release assets of this repo; nothing binary is committed. How apps check and how a release is published:
[docs/RELEASES.md](docs/RELEASES.md).

<!-- index:start (tools/publish writes this table) -->
| App | Platform | Latest | Details |
|---|---|---|---|
| CC Companion | Android 10+ | [1.2.6](https://github.com/neil-bh/app-releases/releases/download/cc-companion-v1.2.6/ClaudeControlCompanion-1.2.6.apk) (2026-11-19) | [apps/cc-companion](apps/cc-companion/README.md) |
| Claude Control for Windows | Windows 10/11 (64-bit) | [1.3.3](https://github.com/neil-bh/app-releases/releases/download/claude-control-windows-v1.3.3/ClaudeControl-1.3.3.exe) (2026-11-19) | [apps/claude-control-windows](apps/claude-control-windows/README.md) |
| Family Game Night | Android (arm64) | [454186](https://github.com/neil-bh/app-releases/releases/download/family-game-night-b454186/family-game-night-b454186.apk) (2026-11-12) | [apps/family-game-night](apps/family-game-night/README.md) |
| RBV Control | Windows 10/11 (64-bit) | [1.4.0](https://github.com/neil-bh/app-releases/releases/download/rbv-control-v1.4.0/RBVControl-1.4.0.exe) (2026-11-18) | [apps/rbv-control](apps/rbv-control/README.md) |
| Tunnel Control | Windows 10/11 (64-bit) | [1.8.0](https://github.com/neil-bh/app-releases/releases/download/tunnel-control-v1.8.0/TunnelControl-1.8.0.exe) (2026-11-18) | [apps/tunnel-control](apps/tunnel-control/README.md) |
<!-- index:end -->

Publishing: `tools/publish <app-id> <version> <file> --changelog <the app's CHANGELOG.json> --notes-from-changelog`
(`--dry-run` first). `tools/check` validates every app folder; `tools/test` tests both.
