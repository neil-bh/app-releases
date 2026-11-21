# Plan: migrate app-releases onto the project baseline (2026-11-21)

Profile: `custom` (Python standard-library tools, JSON data, no profile fits).

| Step | What | Verified by |
|---|---|---|
| CLAUDE.md | New file (there was none): project facts and rules for this repo, then the template's Operating model verbatim, working rules, host section. 127 lines | `baseline-check` |
| Rules moved/kept | Nothing removed: there was no earlier CLAUDE.md. Publishing/secret-scan/new-app rules written from `docs/RELEASES.md` and this session's decisions | read-through |
| Settings | `.claude/settings.json` = skeleton SessionStart hook, word for word; `tools/session-start` is the skeleton's no-op | session start line |
| State | `docs/STATUS.md`, `docs/DECISIONS.md` (decisions carried over, dated), `docs/learnings.md`, `docs/plans/` | state claims checked against live URLs and gates earlier this session |
| Gate | `tools/check` already exists (validator); now a clean no-argument run also runs `tools/test` and writes the gate stamp; `APP_RELEASES_IN_TEST` stops the loop | pass now; break something on purpose and see exit 1 |
| Git | `.gitattributes` `tools/* text eol=lf`; `.gitignore` secrets block via `baseline-update --apply` | `baseline-check` |
| Marker | `.baseline` last | `baseline-check` clean |
