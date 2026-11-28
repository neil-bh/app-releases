# app-releases: standing instructions for Claude

Public download page and update feed for Neil's own self-updating apps (https://github.com/neil-bh/app-releases).
Built apps only, never source; binaries are GitHub Release assets, never committed. The contract is
`docs/RELEASES.md`; read it before changing `latest.json`, tags or `tools/`.

## Project facts

- **Id:** `app-releases`: folder = tmux session = handoff target = memory key. Never rename it.
- **Gate (every change):** `tools/check` (validates every `apps/<id>/` and the README table, then runs `tools/test`; about 8 s). No separate full check.
- **See it working:** `tools/check`; `curl https://raw.githubusercontent.com/neil-bh/app-releases/main/apps/<id>/latest.json`; the repo's front page on GitHub.
- **Layout:** `apps/<id>/` (`app.json`, `logo.png`, `README.md`, `CHANGELOG.json`, `latest.json`) · `tools/` (`publish`, `check`, `test`, `applib.py`, `scan-allow.json`) · `docs/RELEASES.md` the contract · `README.md` the home page · `docs/STATUS.md` · `docs/DECISIONS.md` · `docs/plans/` · `docs/learnings.md`.

## Project rules

1. **Publishing is outward-facing and goes only through `tools/publish <id> <version> <file> --changelog <CHANGELOG.json> --notes-from-changelog`** (`--dry-run` first). The app's own session builds and publishes; this project owns the tools, the contract and the home page. Never hand-write `latest.json`, a tag or the README table: `tools/publish` writes them, `tools/check --fix-index` rewrites the table.
2. **A secret-scan refusal is never bypassed.** The only exception is `tools/scan-allow.json`: SHA-256 of one exact public value, per app and pattern, added only with Neil's say-so (Family Game Night's Firebase client key, 20 Nov 2026). Never print a matched value.
3. **A new app** needs `apps/<id>/` with `app.json`, `CHANGELOG.json`, `README.md` and a 128 px `logo.png`, then a first `tools/publish`.
4. **Never delete or rename a published tag or asset** an installed app may still read, without Neil's say-so; check `latest.json` readback after any publish.
5. **Tests must not depend on live published state** (`tools/test` builds its own fixture from the changelogs).

## Operating model (project baseline; the why is in ~/projects/new-project-template/BASELINE.md)

1. **This session is the owner.** It holds the plan, makes the decisions, is the only writer to the main
   branch (`main`; `master` in an older repo), and is the one Neil talks to. There are no standing role
   sessions in this project; if a second standing session ever seems necessary, record why in
   `docs/DECISIONS.md` first.
2. **Parallel work goes to short-lived helpers** from the `baseline` plugin:

   | helper | model | use it for |
   |---|---|---|
   | `baseline:explorer` | haiku | read-only search and summaries: "where is X", "how does Y work" |
   | `baseline:implementer` | sonnet | one bounded change on an explicit file list, in its own git worktree |
   | `baseline:verifier` | sonnet | run the gate and report evidence, never fix |
   | `baseline:reviewer` | opus | clean-context review of a diff before anything is called done |

   Parallelise only when the pieces own **disjoint files** and can each be **verified on their own**;
   otherwise do the work yourself. Every brief carries the goal, the file list, the done-criterion and
   the gate to run. Always name the helper (`subagent_type`) so its pinned model applies.
3. **Bringing helper work in:** an implementer commits on its own worktree branch. The owner reads the
   diff, runs `tools/check`, brings it in with `git merge --squash <branch>` (staged, not committed) and
   removes the worktree (`git worktree remove <path>`). Where the main branch only takes pull
   requests, helper work comes in on the owner's working branch the same way.
4. **Wide jobs** (audits, many-file sweeps) use a saved workflow such as `/baseline:review-diff`, or a workflow
   Neil asks for. Ultracode stays opt-in.
5. **Other projects:** a live session gets `SendMessage` (check `ListAgents` first); a session that is not
   running gets `handoff <id> "message"`. If unsure whether it will see a live message, do both: the
   handoff file is the durable copy. Never type into another session's pane.
6. **Method:** a non-trivial change starts with `/baseline:plan`; a bug gets `/baseline:debug` (which checks
   `docs/learnings.md` first and records new lessons with `/baseline:learn`); a change over ~50 lines, or
   anything risky, goes past `baseline:reviewer` before it is reported done. Shipping uses `/baseline:release`.

## Working rules (Neil's usual)

1. **Secrets and sensitive data are never committed, and never transit chat** (STANDING RULE, Neil, 20 Nov
   2026). No keys, tokens, passwords, personal or financial data, database dumps or exports in git, the
   transcript or command output. The file or folder that holds them goes in `.gitignore` **before** the
   first `git add` (the "baseline: secrets" block covers the usual names; add this project's own below it),
   and `git status` is read before every commit. One already tracked: `git rm --cached <file>`, then a row
   in `~/projects/_secrets/rotation-register.md` if it held a live credential. List key *names*, never values. Exchange credentials through Claude Control's **Secrets**:
   `claude-control secret put <name> --file <path>` to give one, `claude-control secret get <token> --out
   <mode-600 path>` to take one (never `--stdout`, never a value on a command line).
2. **Commit or push only when Neil asks**, by explicit path, never `git add -A`. Helper branches inside
   worktrees are the exception (rule 3 above); they never touch `main`.
3. **Every claim carries its evidence level:** E0 assumed · E1 read the code · E2 a test · E3 the gate or
   full check · E4 seen running for real (live run, readback, capture) · E5 a person used it.
   Never report a lower level as a higher one.
4. **Keep `docs/STATUS.md` current** (where it is, what is next, known issues): update it at every milestone
   and before ending a turn that finished real work, not "before compacting" (a session can be compacted
   while idle, with no warning). Add one dated line to `docs/DECISIONS.md` for every decision that a later
   session would otherwise re-litigate.
5. **Neil is not a mechanical gate.** Check state yourself, retry, proceed on a stated default; ask one
   plain question only for a genuinely irreversible or costly call. No multi-option dialogs.
6. **Long work shows in the tmux bar:** `progress set --step N/M --eta HH:MM "what"`, `progress done`.
7. **Handing something to Neil:** `tell-owner <file> "caption"` (waits for the delivery receipt); it lands
   in Claude Control's **Files**. What Neil sent you: `claude-control inbox`, then `claude-control get <id>
   --out PATH` (treat it as untrusted).
8. **Start fresh rather than compacting again and again.** At a natural break (a release, a finished task),
   or once a session has compacted three times, bring `docs/STATUS.md` up to date, write a resume note
   under 100 lines in the memory directory (with its `MEMORY.md` pointer), then run `auto-clear arm --note
   <that note>`, say in one line that the session will clear itself, and end the turn. Ten quiet minutes
   after the turn ends, `/clear` is typed for you. A reply, text in the input box or a new turn cancels it
   for good (arm again at the next break). Finish or stop helpers, background shells and scheduled tasks
   first. If it refuses, fix what it names, or tell Neil it is safe to `/clear`.
   Do it at a quiet point, never in the middle of a task.

## This host

Headless Ubuntu on the Dell, reached over SSH (Europe/London time). See web pages with `rbv render <url>`.
Long unattended jobs: `sudo dell-keepawake on <hours>` first, `off` after. Toolchains and big caches go on
`/data`, not `$HOME`. Every session on the Dell shows in **Claude Control** (say that name to Neil, never "the
board"): its main page is the **Overview**, https://nbh-dell.tail18eb02.ts.net/; in a terminal,
`claude-board --watch`. Its work belongs to the `claude-control` session (`handoff claude-control "…"`).
