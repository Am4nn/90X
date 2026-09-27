"""Download raw sources into .data/<domain>/<name>/. Safe to re-run: finished
sources are skipped or updated, and HF downloads resume where they stopped."""

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import urljoin

import httpx
from huggingface_hub import snapshot_download

from .config import DATA_DIR
from .sources import Source

MANIFEST = DATA_DIR / "manifest.json"


def dest_for(src: Source) -> Path:
    return DATA_DIR / src.domain / src.name


def _hf(src: Source, dest: Path) -> None:
    snapshot_download(repo_id=src.target, repo_type="dataset", local_dir=dest, max_workers=8)


def _git(src: Source, dest: Path) -> None:
    if (dest / ".git").exists():
        # A repo exported by _export_windows_safe has no working tree to pull into.
        if subprocess.run(["git", "-C", str(dest), "pull", "--ff-only", "--quiet"]).returncode:
            _export_windows_safe(dest)
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://github.com/{src.target}.git"
    subprocess.run(["git", "clone", "--depth", "1", "--quiet", "--no-checkout", url, str(dest)], check=True)
    if src.paths:
        # Only some of the tree is wanted. Check out with no pathspec: a
        # pathspec overrides the skip-worktree bits and materialises everything.
        subprocess.run(["git", "-C", str(dest), "sparse-checkout", "set", "--no-cone", *src.paths], check=True)
        subprocess.run(["git", "-C", str(dest), "checkout", "--quiet", "HEAD"], check=True)
        return
    # git exits 0 even when it skips files with invalid names, so check stderr too.
    co = subprocess.run(["git", "-C", str(dest), "checkout", "--quiet", "HEAD", "--", "."],
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if co.returncode or "invalid path" in co.stderr:
        _export_windows_safe(dest)


def _export_windows_safe(dest: Path) -> None:
    """Some repos have file names Windows can't hold (':' or '?'). Write each
    file from git objects with those characters replaced by '_'."""
    files = subprocess.run(
        ["git", "-C", str(dest), "ls-tree", "-r", "-z", "--name-only", "HEAD"],
        check=True, capture_output=True,
    ).stdout.decode("utf-8").split("\0")
    for name in filter(None, files):
        safe = Path(*(re.sub(r'[<>:"|?*]', "_", part).rstrip(" .") for part in name.split("/")))
        blob = subprocess.run(
            ["git", "-C", str(dest), "cat-file", "blob", f"HEAD:{name}"], check=True, capture_output=True,
        ).stdout
        out = dest / safe
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(blob)


def _fetch(client: httpx.Client, url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 0:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    with client.stream("GET", url) as r:
        r.raise_for_status()
        with tmp.open("wb") as f:
            for chunk in r.iter_bytes():
                f.write(chunk)
    tmp.replace(path)


def _url(src: Source, dest: Path) -> None:
    with httpx.Client(follow_redirects=True, timeout=60) as client:
        _fetch(client, src.target, dest / Path(src.target).name)


def _url_index(src: Source, dest: Path) -> None:
    """Fetch an index page and download every PDF it links to."""
    with httpx.Client(follow_redirects=True, timeout=60) as client:
        html = client.get(src.target).text
        links = sorted(set(re.findall(r'href="?([^" >]+\.pdf)', html, re.IGNORECASE)))
        for link in links:
            _fetch(client, urljoin(src.target, link), dest / Path(link).name)


def _url_links(src: Source, dest: Path) -> None:
    """Fetch an index page and save every page it links to matching link_pattern."""
    pattern = re.compile(f'href="({src.link_pattern})"')
    with httpx.Client(follow_redirects=True, timeout=60, headers={"user-agent": "90x-pipeline"}) as client:
        index = client.get(src.target).text
        (dest / "_index.html").parent.mkdir(parents=True, exist_ok=True)
        (dest / "_index.html").write_text(index, encoding="utf-8")
        for link in sorted(set(pattern.findall(index))):
            _fetch(client, urljoin(src.target, link), dest / f"{PurePosixPath(link).name}.html")


HANDLERS = {"hf": _hf, "git": _git, "url": _url, "url_index": _url_index, "url_links": _url_links}


def _dir_size(path: Path) -> int:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file() and ".git" not in f.parts)


def _load_manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def download(sources: list[Source]) -> list[str]:
    """Download each source. Returns names that failed; the rest still finish."""
    manifest = _load_manifest()
    failed = []
    for i, src in enumerate(sources, 1):
        dest = dest_for(src)
        print(f"[{i}/{len(sources)}] {src.domain}/{src.name} ({src.kind}: {src.target})", flush=True)
        try:
            HANDLERS[src.kind](src, dest)
        except Exception as e:  # keep going; report at the end
            print(f"    FAILED: {e}", flush=True)
            failed.append(src.name)
            continue
        size = _dir_size(dest)
        print(f"    ok, {size / 1e6:.1f} MB", flush=True)
        manifest[src.name] = {
            "domain": src.domain,
            "kind": src.kind,
            "target": src.target,
            "role": src.role,
            "path": str(dest.relative_to(DATA_DIR)),
            "bytes": size,
            "downloaded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        MANIFEST.write_text(json.dumps(manifest, indent=2))
    return failed
