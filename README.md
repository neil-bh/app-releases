# app-releases

Public downloads for test builds of private projects. Built apps only (APKs and similar), never source code.

Each app's releases share a tag prefix, so one repo can serve several apps:

| Tag prefix | App |
|---|---|
| `family-game-night-b<build>` | Party phrase game (Android test builds) |

Apps check this repo for a newer release and offer it in-app. The build number is minutes since 2026-01-01 UTC, so it always increases.
