# Decisions: app-releases

One dated line per decision a later session would otherwise re-open: what was decided, and why.
Newest at the bottom. Only the owner session writes here.

- 2026-11-18: One public repo for every self-updating app; apps read `raw.githubusercontent.com/.../apps/<id>/latest.json` (CDN, no API rate limit), verify size and SHA-256, and fall back to the Dell only when GitHub is unreachable (contract: `docs/RELEASES.md`).
- 2026-11-18: Only `tools/publish` creates releases and writes `latest.json`, the app README's Latest line and the home-page table.
- 2026-11-20: Uniform tags and assets for every app (`<id>-v<version>`, `<AssetName>-<version>.<ext>`); Family Game Night moved to it, old `-b` tags deleted with Neil's consent.
- 2026-11-20: Secret-scan allowlist, hash only, per app and pattern, for Family Game Night's public Firebase client key (Neil approved). Everything else still blocks.
- 2026-11-20: The home page is the README table (logo, one-liner, platform, latest, date, download); each app has a 128 px `logo.png`.
- 2026-11-21: `tools/check` is the project gate: it validates, then runs `tools/test` (skipped when `APP_RELEASES_IN_TEST` is set).
- 2026-11-21: Migrated to project baseline 0.64.0.
