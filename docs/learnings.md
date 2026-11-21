# Learnings: app-releases

Hard-won lessons, newest first, written with `/baseline:learn`: symptom, cause, fix/rule, evidence.
Search here before debugging.

## 2026-11-20: tests that read the live repo rot
Symptom: 7 tests failed with no code change. Cause: the fixture copied the working tree, so published state (latest.json files, a withdrawn release) leaked into assertions. Fix: the fixture strips latest.json and rebuilds Family Game Night's from its changelog. Evidence: E2, `tools/test`.

## 2026-11-20: a published asset can vanish from GitHub while latest.json still points at it
Family Game Night's old release was deleted; `latest.json` kept a dead URL (404). `tools/check` does not fetch URLs, so check readback (HTTP 200) after any release deletion.
