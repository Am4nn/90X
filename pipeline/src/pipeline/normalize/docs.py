"""Turn every Markdown (and PDF) source into readable Library documents.

Large files are split at H1-H3 headings (code fences respected); sections too
short to stand alone are merged into the one before. Relative links and
images are rewritten to GitHub URLs so they render in the app."""

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from ..config import DATA_DIR
from ..sources import SOURCES

HEADING = re.compile(r"^(#{1,3})\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)([^)]*)\)")
SKIP_FILES = re.compile(r"(?i)(contributing|code_of_conduct|license|changelog|translations?|security)\.md$|readme-[a-z]{2}")


@dataclass
class Section:
    title: str
    body: str


@dataclass(frozen=True)
class DocSet:
    source: str            # name in sources.py
    domain: str
    include: tuple[str, ...]
    exclude: tuple[str, ...] = ()


# What each source contributes to the Library, and to which area.
DOC_SETS = (
    DocSet("system-design-primer", "system_design", ("README.md", "solutions/system_design/*/README.md")),
    DocSet("system-design-karan", "system_design", ("README.md",)),
    DocSet("system-design-101", "system_design", ("**/*.md",), ("translations/**",)),
    DocSet("grokking-system-design", "system_design", ("**/*.md",)),
    DocSet("cs-fundamentals-interview", "system_design", ("System_Design/**/*.md",)),
    DocSet("cs-fundamentals-interview", "cs", ("OS_COA/**/*.md", "DBMS/**/*.md", "CN/**/*.md", "OOPS/**/*.md", "REST_API/**/*.md")),
    DocSet("last-minute-notes", "cs", ("CN.md", "DBMS.md", "OS.md", "OOPS.md")),
    DocSet("last-minute-notes", "sql", ("SQL.md",)),
    DocSet("last-minute-notes", "behavioral", ("INTERVIEW.md",)),
    DocSet("devops-exercises", "cs", ("topics/linux/**/*.md", "topics/os/**/*.md", "topics/databases/**/*.md", "topics/dns/**/*.md")),
    DocSet("devops-exercises", "sql", ("topics/sql/**/*.md",)),
    DocSet("java-basics", "java", ("*.md",)),
    DocSet("java-interview-guide", "java", ("README.md",)),
    DocSet("java-interview-devinterview", "java", ("README.md",)),
    DocSet("sql-basics", "sql", ("*.md",)),
    DocSet("grokking-ood", "lld", ("docs/**/*.md", "object-oriented-design-case-studies/*.md")),
    DocSet("awesome-lld", "lld", ("**/*.md",), ("solutions/**",)),
    DocSet("aiml-interviews", "ai", ("src/**/*.md",)),
    DocSet("ml-interviews-book", "ai", ("contents/**/*.md",)),
    DocSet("llm-interview-questions", "ai", ("README.md",)),
    DocSet("data-science-interview", "ai", ("*.md",)),
    DocSet("tech-interview-handbook", "behavioral", ("apps/website/contents/**/*.md",)),
    DocSet("big-companies-interview-questions", "behavioral", ("companies/**/*.md",)),
)

# PDFs: one document per file.
PDF_SETS = (("ostep", "cs"), ("little-book-of-semaphores", "cs"))


def split_markdown(text: str, min_chars: int = 400) -> list[Section]:
    sections: list[Section] = []
    current_h2 = None
    title, lines, in_fence = None, [], False

    def flush():
        body = "\n".join(lines).strip()
        if title is None and not body:
            return
        if sections and len(body) < min_chars:
            # Too short to stand alone: fold into the previous section, heading and all.
            heading = f"\n\n### {title.split(' › ')[-1]}\n\n" if title else "\n\n"
            sections[-1].body = f"{sections[-1].body}{heading}{body}".strip()
        else:
            sections.append(Section(title or "Introduction", body))

    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
        m = None if in_fence else HEADING.match(line)
        if m:
            flush()
            level, heading = len(m.group(1)), m.group(2).strip()
            if level <= 2:
                current_h2 = heading if level == 2 else None
                title = heading
            else:
                title = f"{current_h2} › {heading}" if current_h2 else heading
            lines = []
        else:
            lines.append(line)
    flush()
    return sections


def rewrite_links(body: str, repo: str, file_dir: str) -> str:
    def fix(m: re.Match) -> str:
        bang, text, target, rest = m.groups()
        if re.match(r"^(https?:|mailto:|#|data:)", target):
            return m.group(0)
        path = str(PurePosixPath(file_dir, target)) if file_dir else target
        path = re.sub(r"(^|/)\./", r"\1", path)
        base = "https://raw.githubusercontent.com" if bang else "https://github.com"
        mid = "HEAD" if bang else "blob/HEAD"
        return f"{bang}[{text}]({base}/{repo}/{mid}/{path}{rest})"

    return LINK.sub(fix, body)


def doc_id(source: str, path: str, title: str, n: int) -> str:
    digest = hashlib.sha1(f"{path}#{title}#{n}".encode()).hexdigest()[:16]
    return f"{source}:{digest}"


def _files(root: Path, docset: DocSet) -> list[Path]:
    found: set[Path] = set()
    for pattern in docset.include:
        found.update(p for p in root.glob(pattern) if p.is_file())
    excluded = {p for pattern in docset.exclude for p in root.glob(pattern)}
    return sorted(p for p in found - excluded if ".git" not in p.parts and not SKIP_FILES.search(p.name))


def build_documents() -> list[dict]:
    by_name = {s.name: s for s in SOURCES}
    rows: list[dict] = []
    for docset in DOC_SETS:
        src = by_name[docset.source]
        root = DATA_DIR / src.domain / src.name
        for file in _files(root, docset):
            rel = file.relative_to(root).as_posix()
            text = file.read_text(encoding="utf-8", errors="replace")
            text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
            for n, sec in enumerate(split_markdown(text)):
                if len(sec.body) < 80:
                    continue
                title = sec.title if sec.title != "Introduction" else PurePosixPath(rel).stem.replace("-", " ").replace("_", " ")
                rows.append({
                    "id": doc_id(docset.source, rel, sec.title, n),
                    "domain": docset.domain,
                    "title": title[:300],
                    "body_md": rewrite_links(sec.body, src.target, str(PurePosixPath(rel).parent) if "/" in rel else ""),
                    "url": f"https://github.com/{src.target}/blob/HEAD/{rel}",
                    "source_id": docset.source,
                    "sort": n,
                    "path": rel,
                })
    rows.extend(_pdf_documents(by_name))
    return rows


PDF_PART_CHARS = 40_000


def split_long_text(text: str, limit: int = PDF_PART_CHARS) -> list[str]:
    """Split at paragraph breaks into parts of at most ~limit characters."""
    # PDF text often has no blank lines; fall back to single line breaks for
    # any paragraph that is itself over the limit.
    pieces: list[tuple[str, str]] = []
    for para in text.split("\n\n"):
        if len(para) > limit:
            pieces.extend((line, "\n") for line in para.split("\n"))
        else:
            pieces.append((para, "\n\n"))

    parts, current = [], ""
    for piece, sep in pieces:
        if current and len(current) + len(piece) > limit:
            parts.append(current.strip())
            current = ""
        current += piece + sep
    if current.strip():
        parts.append(current.strip())
    return parts


def _pdf_documents(by_name) -> list[dict]:
    import logging

    from pypdf import PdfReader

    logging.getLogger("pypdf").setLevel(logging.ERROR)

    rows = []
    for name, domain in PDF_SETS:
        src = by_name[name]
        root = DATA_DIR / src.domain / src.name
        for n, file in enumerate(sorted(root.glob("*.pdf"))):
            try:
                text = "\n".join((page.extract_text() or "") for page in PdfReader(file).pages)
            except Exception as e:  # a broken PDF shouldn't stop the run
                print(f"  skip {file.name}: {e}")
                continue
            text = re.sub(r"[ \t]+\n", "\n", text).strip()
            if len(text) < 200:
                continue
            first = next((line.strip() for line in text.splitlines() if len(line.strip()) > 3), file.stem)
            base = src.target if src.target.startswith("http") and src.target.endswith("/") else ""
            title = f"{file.stem.replace('-', ' ').title()}: {first}" if name == "ostep" else first
            parts = split_long_text(text)
            for part_no, part in enumerate(parts):
                suffix = f" (part {part_no + 1} of {len(parts)})" if len(parts) > 1 else ""
                rows.append({
                    "id": doc_id(name, file.name, file.stem, part_no),
                    "domain": domain,
                    "title": f"{title[:280]}{suffix}",
                    "body_md": part,
                    "url": f"{base}{file.name}" if base else src.target,
                    "source_id": name,
                    "sort": n * 100 + part_no,
                    "path": file.name,
                })
    return rows


def run(con) -> int:
    rows = build_documents()
    con.execute("delete from documents")
    con.executemany(
        "insert into documents (id, domain, title, body_md, url, source_id, sort, path) values (?, ?, ?, ?, ?, ?, ?, ?)",
        [[r["id"], r["domain"], r["title"], r["body_md"], r["url"], r["source_id"], r["sort"], r["path"]] for r in rows],
    )
    return len(rows)
