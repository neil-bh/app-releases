# Releases: the contract

This repo is **public**. It holds built apps and their release notes for private projects, never source. Everything
here (READMEs, changelogs, `latest.json`, the binaries on the Releases page) can be read and downloaded by anyone, so
a build must contain nothing secret: `tools/publish` refuses a file with secret-shaped strings in it.

## Layout

```
apps/<app-id>/
  app.json        who the app is: id, name, platform, ext, asset_name, summary, min_os?, tag?, asset?
  README.md       what it is, how to install and update it; its "Latest" line is written by tools/publish
  CHANGELOG.json  {app: <app-id>, entries: [{version, date, title, notes[]}]}, newest first
  latest.json     what an app reads to update itself (below); present once something is published
  ...             any other release document (install guide, screenshots, known issues) may sit beside these
tools/            publish, check, test (Python standard library)
docs/RELEASES.md  this file
README.md         index of the apps; its table is written by tools/publish
```

Binaries are **GitHub Release assets**, never committed (`tools/check` fails if one is). Each release is tagged
`<app-id>-v<version>` and its one asset is named `<asset_name>-<version>.<ext>` (e.g. `tunnel-control-v1.7.1` /
`TunnelControl-1.7.1.exe`). An app may keep an older scheme through `tag`/`asset` templates in its `app.json`:
Family Game Night keeps `family-game-night-b<build>` / `family-game-night-b<build>.apk`, which its in-app updater
already depends on.

| App id | App | Platform |
|---|---|---|
| `claude-control-windows` | Claude Control for Windows | Windows |
| `cc-companion` | CC Companion (Claude Control Companion) | Android |
| `tunnel-control` | Tunnel Control | Windows |
| `rbv-control` | RBV Control | Windows |
| `family-game-night` | Family Game Night | Android |

## latest.json

```json
{"app": "tunnel-control", "version": "1.7.1", "tag": "tunnel-control-v1.7.1", "asset": "TunnelControl-1.7.1.exe",
 "url": "https://github.com/neil-bh/app-releases/releases/download/tunnel-control-v1.7.1/TunnelControl-1.7.1.exe",
 "sha256": "<64 hex>", "size": 13095424, "date": "2026-11-18", "notes_title": "Tidies up after older versions",
 "min_os": "Windows 10"}
```

`version` is numbers and dots and is always the newest `CHANGELOG.json` entry; `notes_title` is that entry's title;
`url` is exactly `https://github.com/neil-bh/app-releases/releases/download/<tag>/<asset>`; `min_os` is optional.

## How an app checks for an update

1. `GET https://raw.githubusercontent.com/neil-bh/app-releases/main/apps/<app-id>/latest.json`
   (a few seconds' timeout; raw.githubusercontent.com is a CDN with no API rate limit, unlike api.github.com's 60
   unauthenticated calls an hour, so checking every few hours from every device is fine. It may serve a copy up to
   about 5 minutes old.)
2. Check the JSON: `app` is this app's id, `version` is numbers and dots, `sha256` is 64 hex digits, `size` is
   believable, and `url` starts with `https://github.com/neil-bh/app-releases/releases/download/`. Anything else:
   treat as "cannot check", never as "up to date".
3. Compare `version` with the running version numerically, part by part (`1.10.0` is newer than `1.9.0`).
4. When newer: download `url` (GitHub redirects to its storage host; follow redirects, HTTPS only), up to `size`
   bytes and no more.
5. **Verify the size and the SHA-256 of the downloaded bytes before running, installing or swapping anything.** A
   mismatch is a failed update, said plainly; the download is deleted.
6. Install as the app already does (swap and restart on Windows, the package installer on Android).

Never put a token in an app: the repo is public and needs none. If GitHub cannot be reached, an app may fall back
to its old source (the Dell, over Tailscale) and say where the update came from.

## Publishing a release

Only from the Dell, by the owner (or with his go-ahead): it is an outward publication.

```
tools/publish <app-id> <version> <file> --changelog <the app's own CHANGELOG.json> --notes-from-changelog --dry-run
tools/publish <app-id> <version> <file> --changelog <the app's own CHANGELOG.json> --notes-from-changelog
```

It refuses unless the changelog's newest entry is `<version>`, the file is the app's kind, and a scan of its strings
(ASCII and UTF-16, and every member of an APK/zip) finds no private key, GitHub/Tailscale/Anthropic/OpenAI/AWS/Slack/
Google token, JWT, bearer token or `password=`-style assignment (it prints only the pattern's name and offset). Then
it creates the release (not marked as the repo's Latest: the repo serves several apps), reads it back to check the
asset, writes `latest.json`, `CHANGELOG.json` and both READMEs, commits those paths and pushes. Apps see the release
once the push lands. A version is never re-published: publish a new version instead.

`tools/check` validates every app folder offline; `tools/test` tests both tools with a fake `gh` (never GitHub).

Family Game Night still publishes with its own `scripts/release_apk.sh` and lists `api.github.com/.../releases?per_page=50`
filtered by its tag prefix; it does not read `latest.json` yet. Its folder here is kept for the index and changelog.
Because that list is shared by every app, once this repo has more than about 45 other releases newer than the
game's latest, the game would stop seeing its own: moving it to `latest.json` removes that limit.
