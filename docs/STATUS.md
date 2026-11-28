# Status: app-releases

_Updated 2026-11-21._

## Where it is
- All 5 self-updating apps are published and read back (E4, 28 Nov: every `latest.json` URL downloads, size and SHA-256 match, raw feed equals the repo): Claude Control for Android 1.13.3 (id `claude-control-android`; `cc-companion` is its mirrored legacy feed), Claude Control for Windows 1.7.10, RBV Control 1.4.0, Tunnel Control 1.8.0, Family Game Night 465260. The first four match their source projects' newest changelog entry.
- `README.md` is the home page: logo, one-liner, platform, latest, date and download per app (written by `tools/publish`; `tools/check` fails if stale). Logos refreshed 28 Nov for the two Claude Control apps' new CC icon; `tools/logo <id> <icon>` makes a logo.
- `tools/publish` secret-scans every build; one exact public Firebase key is allowed for Family Game Night only (`tools/scan-allow.json`).

## Next
1. Family Game Night has 13 commits since build 465260; its session was asked on 28 Nov to publish a new build.
2. When an app's icon changes, refresh its logo with `tools/logo` in the same push as its release.

## Known issues
- Neil still has to confirm in Google Cloud that the Firebase key is restricted to the app's package name and signing SHA-1 (the allowlist assumes it).
