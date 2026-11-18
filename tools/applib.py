"""applib: the shared part of tools/publish and tools/check (docs/RELEASES.md is the contract). Standard library only.

Every app lives in apps/<id>/:
  app.json        who it is: {id, name, platform, ext, asset_name, tag?, asset?, min_os?, summary}
  README.md       what it is and how to install it; its "Latest" line is written by tools/publish
  CHANGELOG.json  {app: <id>, entries: [{version, date, title, notes[]}]}, newest first
  latest.json     {app, version, tag, asset, url, sha256, size, date, notes_title, min_os?} once something is published
The binaries themselves are GitHub Release assets, never committed.
"""
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
REPO = os.environ.get("APP_RELEASES_REPO") or "neil-bh/app-releases"
BRANCH = "main"
ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{1,40}")
VER_RE = re.compile(r"\d{1,9}(\.\d{1,6}){0,3}")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
SHA_RE = re.compile(r"[0-9a-f]{64}")
EXT_RE = re.compile(r"[a-z0-9]{1,8}")
NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,60}")
DEFAULT_TAG = "{id}-v{version}"
DEFAULT_ASSET = "{asset_name}-{version}.{ext}"
LATEST_KEYS = ("app", "version", "tag", "asset", "url", "sha256", "size", "date", "notes_title")
INDEX_START, INDEX_END = "<!-- index:start (tools/publish writes this table) -->", "<!-- index:end -->"
LATEST_START, LATEST_END = "<!-- latest:start (tools/publish writes this line) -->", "<!-- latest:end -->"
MAX_SIZE = 500 * 1048576


class Problem(Exception):
    pass


# ------------------------------------------------------------------------------------------------ versions and files
def vkey(v):
    return tuple(int(x) for x in str(v).split("."))


def vcmp(a, b):
    x, y = vkey(a), vkey(b)
    n = max(len(x), len(y))
    x, y = x + (0,) * (n - len(x)), y + (0,) * (n - len(y))
    return (x > y) - (x < y)


def app_dir(app_id, root=ROOT):
    return os.path.join(root, "apps", app_id)


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    tmp = f"{path}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def app_ids(root=ROOT):
    d = os.path.join(root, "apps")
    return sorted(x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))) if os.path.isdir(d) else []


def load_app(app_id, root=ROOT):
    if not ID_RE.fullmatch(app_id or ""):
        raise Problem(f"{app_id!r} is not an app id (lower case, digits and dashes)")
    p = os.path.join(app_dir(app_id, root), "app.json")
    try:
        a = read_json(p)
    except FileNotFoundError:
        raise Problem(f"no app {app_id!r}: apps/{app_id}/app.json is missing (known: {', '.join(app_ids(root)) or 'none'})")
    except ValueError as e:
        raise Problem(f"apps/{app_id}/app.json is not JSON: {e}")
    errs = check_app(a, app_id)
    if errs:
        raise Problem(f"apps/{app_id}/app.json: " + "; ".join(errs))
    return a


def check_app(a, app_id):
    errs = []
    if not isinstance(a, dict):
        return ["not an object"]
    if a.get("id") != app_id:
        errs.append(f"id must be {app_id!r}")
    for k in ("name", "platform", "summary"):
        if not isinstance(a.get(k), str) or not a[k].strip():
            errs.append(f"{k} must be a non-empty string")
    if not EXT_RE.fullmatch(str(a.get("ext", ""))):
        errs.append("ext must be a file extension (apk, exe, ...)")
    if not NAME_RE.fullmatch(str(a.get("asset_name", ""))):
        errs.append("asset_name must be a plain file name stem")
    for k in ("tag", "asset"):
        if k in a and (not isinstance(a[k], str) or "{version}" not in a[k]):
            errs.append(f"{k} must be a template containing {{version}}")
    if "min_os" in a and not isinstance(a["min_os"], str):
        errs.append("min_os must be a string")
    return errs


def tag_for(a, version):
    return a.get("tag", DEFAULT_TAG).format(id=a["id"], version=version)


def asset_for(a, version):
    return a.get("asset", DEFAULT_ASSET).format(id=a["id"], version=version, asset_name=a["asset_name"], ext=a["ext"])


def url_for(tag, asset, repo=REPO):
    return f"https://github.com/{repo}/releases/download/{tag}/{asset}"


def readme_url(app_id, repo=REPO):
    return f"https://github.com/{repo}/blob/{BRANCH}/apps/{app_id}/README.md"


def raw_latest_url(app_id, repo=REPO):
    return f"https://raw.githubusercontent.com/{repo}/{BRANCH}/apps/{app_id}/latest.json"


# ------------------------------------------------------------------------------------------------ changelog
def check_changelog(doc, app_id):
    """Problems with a CHANGELOG.json, as sentences ([] when it is fine)."""
    if not isinstance(doc, dict) or not isinstance(doc.get("entries"), list):
        return ["not {app, entries: [...]}"]
    errs = []
    if doc.get("app") != app_id:
        errs.append(f"app must be {app_id!r}, not {doc.get('app')!r}")
    seen, prev = set(), None
    for i, e in enumerate(doc["entries"]):
        where = f"entry {i + 1}"
        if not isinstance(e, dict):
            errs.append(f"{where} is not an object")
            continue
        v = str(e.get("version", ""))
        if not VER_RE.fullmatch(v):
            errs.append(f"{where}: version {v!r} is not numbers and dots")
            continue
        if v in seen:
            errs.append(f"{where}: version {v} appears twice")
        seen.add(v)
        if prev is not None and vcmp(v, prev) >= 0:
            errs.append(f"{where}: {v} is not older than {prev} (newest first)")
        prev = v
        if not DATE_RE.fullmatch(str(e.get("date", ""))):
            errs.append(f"{where} ({v}): date must be YYYY-MM-DD")
        if not isinstance(e.get("title"), str) or not e["title"].strip():
            errs.append(f"{where} ({v}): no title")
        n = e.get("notes")
        if not isinstance(n, list) or not all(isinstance(x, str) for x in n):
            errs.append(f"{where} ({v}): notes must be a list of strings")
    return errs


def normalise_changelog(doc, app_id):
    """A source changelog (each project names its app its own way: "windows", "tunnel", ...) as this repo's: the app
    is the repo's id, and only the contract's fields are kept."""
    if not isinstance(doc, dict) or not isinstance(doc.get("entries"), list):
        raise Problem("the changelog is not {app, entries: [...]}")
    out = {"app": app_id, "entries": []}
    for e in doc["entries"]:
        if isinstance(e, dict):
            out["entries"].append({"version": str(e.get("version", "")), "date": str(e.get("date", "")),
                                   "title": e.get("title"), "notes": e.get("notes") if e.get("notes") is not None else []})
    return out


def notes_text(entry, full):
    if not full:
        return entry["title"]
    return "\n".join([f"**{entry['title']}**", ""] + [f"- {n}" for n in entry["notes"]])


# ------------------------------------------------------------------------------------------------ latest.json
def check_latest(l, a, changelog=None, repo=REPO):
    if not isinstance(l, dict):
        return ["not an object"]
    errs = [f"missing {k}" for k in LATEST_KEYS if k not in l]
    if errs:
        return errs
    v = str(l["version"])
    if l["app"] != a["id"]:
        errs.append(f"app must be {a['id']!r}")
    if not VER_RE.fullmatch(v):
        errs.append(f"version {v!r} is not numbers and dots")
        return errs
    if l["tag"] != tag_for(a, v):
        errs.append(f"tag must be {tag_for(a, v)!r}")
    if l["asset"] != asset_for(a, v):
        errs.append(f"asset must be {asset_for(a, v)!r}")
    if l["url"] != url_for(l["tag"], l["asset"], repo):
        errs.append(f"url must be {url_for(l['tag'], l['asset'], repo)}")
    if not SHA_RE.fullmatch(str(l["sha256"])):
        errs.append("sha256 must be 64 lower-case hex digits")
    if not isinstance(l["size"], int) or isinstance(l["size"], bool) or not 0 < l["size"] <= MAX_SIZE:
        errs.append("size must be a positive whole number of bytes")
    if not DATE_RE.fullmatch(str(l["date"])):
        errs.append("date must be YYYY-MM-DD")
    if "min_os" in l and not isinstance(l["min_os"], str):
        errs.append("min_os must be a string")
    if changelog is not None:
        ents = changelog.get("entries") or []
        if not ents or str(ents[0].get("version")) != v:
            errs.append(f"version {v} is not the newest CHANGELOG entry ({ents[0].get('version') if ents else 'none'})")
        elif l["notes_title"] != ents[0].get("title"):
            errs.append("notes_title is not the newest CHANGELOG entry's title")
    return errs


# ------------------------------------------------------------------------------------------------ READMEs
def latest_line(a, l):
    if not l:
        return "**Latest:** nothing published here yet."
    return (f"**Latest:** [{a['name']} {l['version']}]({l['url']}) ({l['date']}, {l['size'] / 1048576:.1f} MB, "
            f"SHA-256 `{l['sha256']}`) · [all releases](https://github.com/{REPO}/releases?q={a['id']}&expanded=true)")


def with_block(text, start, end, body):
    """text with the block between the two markers replaced (appended, markers and all, when absent)."""
    block = f"{start}\n{body}\n{end}"
    i, j = text.find(start), text.find(end)
    if i >= 0 and j > i:
        return text[:i] + block + text[j + len(end):]
    return text.rstrip("\n") + "\n\n" + block + "\n"


def app_readme(text, a, l):
    return with_block(text, LATEST_START, LATEST_END, latest_line(a, l))


def index_table(root=ROOT):
    rows = ["| App | Platform | Latest | Details |", "|---|---|---|---|"]
    for app_id in app_ids(root):
        try:
            a = load_app(app_id, root)
        except Problem:
            continue
        lp = os.path.join(app_dir(app_id, root), "latest.json")
        l = read_json(lp) if os.path.exists(lp) else None
        latest = f"[{l['version']}]({l['url']}) ({l['date']})" if l else "not published yet"
        rows.append(f"| {a['name']} | {a['platform']} | {latest} | [apps/{app_id}](apps/{app_id}/README.md) |")
    return "\n".join(rows)


def root_readme(text, root=ROOT):
    return with_block(text, INDEX_START, INDEX_END, index_table(root))


# ------------------------------------------------------------------------------------------------ secret scan
# Names only ever leave this module with an offset: a match is never printed, logged or returned.
SECRET_PATTERNS = [
    ("private_key", rb"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----"),
    ("github_token", rb"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b"),
    ("github_pat", rb"\bgithub_pat_[A-Za-z0-9_]{40,}"),
    ("tailscale_key", rb"\btskey-[a-z]+-[A-Za-z0-9]{6,}-[A-Za-z0-9]{10,}"),
    ("anthropic_key", rb"\bsk-ant-[A-Za-z0-9_-]{20,}"),
    ("openai_style_key", rb"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}"),
    ("aws_access_key", rb"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("slack_token", rb"\bxox[abposr]-[A-Za-z0-9-]{10,}"),
    ("google_api_key", rb"\bAIza[0-9A-Za-z_-]{35}\b"),
    ("jwt", rb"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    # a token has digits: Go's packed string tables put "Bearer " right before ordinary words ("Bearer UnknownEllipse...")
    ("bearer_token", rb"\b[Bb]earer (?=[A-Za-z._~+/-]{0,20}\d)[A-Za-z0-9._~+/-]{24,}=*"),
    ("password_assignment", rb"(?i)\b(?:password|passwd|pwd|secret|api_?key|access_?token|auth_?token)\s*[=:]\s*[\"']?(?![\"'%{$<(\[])[^\s\"'%{}$<>]{8,}"),
]
_COMPILED = [(n, re.compile(p)) for n, p in SECRET_PATTERNS]
_RUN_A = re.compile(rb"[\x20-\x7e\t]{6,}")
_RUN_W = re.compile(rb"(?:[\x20-\x7e\t]\x00){6,}")


def _runs(data):
    """(offset, bytes) of every printable run, as `strings -a` and `strings -a -e l` would find them."""
    for m in _RUN_A.finditer(data):
        yield m.start(), m.group()
    for m in _RUN_W.finditer(data):
        yield m.start(), m.group()[::2]


def scan_bytes(data, where=""):
    hits = []
    for off, run in _runs(data):
        for name, rx in _COMPILED:
            for m in rx.finditer(run):
                hits.append((name, f"{where}{off + m.start()}"))
    return hits


def scan_file(path):
    """[(pattern name, offset)] for secret-shaped strings in a file. A zip (APK, JAR, ...) is also scanned member by
    member, decompressed, since its compressed bytes hide them. `strings` is what this does, in Python, so it needs
    nothing installed and the offsets are exact."""
    with open(path, "rb") as f:
        data = f.read()
    hits = scan_bytes(data)
    if data[:2] == b"PK":
        try:
            with zipfile.ZipFile(path) as z:
                for info in z.infolist():
                    if info.file_size > MAX_SIZE:
                        continue
                    hits += scan_bytes(z.read(info), f"{info.filename}:")
        except (zipfile.BadZipFile, OSError, RuntimeError, NotImplementedError):
            pass
    return hits


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def today():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def have(cmd):
    return shutil.which(cmd) is not None
