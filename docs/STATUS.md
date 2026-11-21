# Status: app-releases

_Updated 2026-11-21._

## Where it is
- All 5 self-updating apps are published with a working download and `latest.json`: CC Companion 1.3.3, Claude Control for Windows 1.3.4, RBV Control 1.4.0, Tunnel Control 1.8.0, Family Game Night 465260 (E4: URLs fetched, `tools/check` and `tools/test` pass).
- `README.md` is the home page: a table with logo, one-liner, platform, latest, date and download per app (written by `tools/publish`; `tools/check` fails if stale).
- `tools/publish` secret-scans every build; one exact public Firebase key is allowed for Family Game Night only (`tools/scan-allow.json`).

## Next
1. Nothing pending here. Apps publish from their own sessions; a new self-updating app gets a folder and a first publish.

## Known issues
- Neil still has to confirm in Google Cloud that the Firebase key is restricted to the app's package name and signing SHA-1 (the allowlist assumes it).
