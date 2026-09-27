"""Every raw source 90X downloads. Verified 2026-09-26 (exists, fields, size).

role:
  cards       - cards get generated from it in v1
  enrich      - adds metadata (importance, pattern, video) to other sources
  reference   - downloaded and loaded, no cards yet

Domain "competitive" holds contest problem sets (Codeforces-style). They are a
separate category from interview DSA: long statements, stdin/stdout, and huge
hidden test suites (that's why they're ~18 GB).
"""

from dataclasses import dataclass
from typing import Literal

Kind = Literal["hf", "git", "url", "url_index", "url_links"]
Role = Literal["cards", "enrich", "reference"]


@dataclass(frozen=True)
class Source:
    name: str  # folder name under .data/<domain>/
    domain: str  # dsa, competitive, system_design, lld, cs, ai, behavioral
    kind: Kind
    target: str  # HF repo id, GitHub owner/repo, or URL
    role: Role
    note: str
    size_gb: float = 0.0  # approximate download size
    paths: tuple[str, ...] = ()  # git: sparse-checkout these paths instead of the whole tree
    link_pattern: str = ""  # url_links: regex for the hrefs to follow from the index page


SOURCES: list[Source] = [
    # --- DSA ---
    Source("leetcode-dataset", "dsa", "hf", "newfacade/LeetCodeDataset", "cards",
           "~2.6K LeetCode problems: tags, difficulty, Python solution, tests, explanation. Apache-2.0", 0.1),
    Source("leetcode-detailed", "dsa", "hf", "kaysss/leetcode-problem-detailed", "enrich",
           "Topic tags, acceptance rate, submissions, similar questions. MIT", 0.04),
    Source("leetcode-multilang", "dsa", "hf", "greengerong/leetcode", "enrich",
           "Solutions in Java, C++, Python, JS. MIT", 0.02),
    Source("leetcode-allenhung", "dsa", "hf", "allenhung1025/leetcode", "reference",
           "2.3K problems with multi-language solutions (overlaps greengerong)", 0.01),
    Source("apps-leetcode-codeforces", "dsa", "hf", "xtremekiwi/APPS-leetcode-codeforces", "reference",
           "500 mixed problems with I/O tests. MIT", 0.01),
    Source("neetcode", "dsa", "git", "neetcode-gh/leetcode", "enrich",
           "450 problems in .problemSiteData.json: NeetCode pattern, NC150/Blind75 flags, YouTube id. MIT", 0.02),
    Source("company-wise-liquidslr", "dsa", "git", "liquidslr/leetcode-company-wise-problems", "enrich",
           "Company-wise problem CSVs with frequency", 0.01),
    Source("company-wise-snehasishroy", "dsa", "git", "snehasishroy/leetcode-companywise-interview-questions", "enrich",
           "Company-wise questions, updated July 2026", 0.01),
    Source("leetmap-pro", "dsa", "git", "saitarrun/LeetMap-Pro", "enrich",
           "Company to problem mapping. MIT", 0.01),
    Source("faang-questions", "dsa", "git", "ombharatiya/FAANG-Coding-Interview-Questions", "reference",
           "Curated FAANG lists. GPL-3.0, local use only", 0.0),
    Source("coding-patterns", "dsa", "git",
           "Chanda-Abdul/Several-Coding-Patterns-for-Solving-Data-Structures-and-Algorithms-Problems-during-Interviews",
           "enrich", "Pattern write-ups, source for pattern explainers", 0.0),
    Source("interactive-coding-challenges", "dsa", "git", "donnemartin/interactive-coding-challenges", "reference",
           "120+ Python challenges with notebooks", 0.01),

    # --- Competitive programming (large: hidden test suites) ---
    Source("primeintellect-verifiable", "competitive", "hf", "PrimeIntellect/verifiable-coding-problems", "reference",
           "144K contest problems with gold solutions", 10.8),
    Source("openr1-verifiable-python", "competitive", "hf", "open-r1/verifiable-coding-problems-python", "reference",
           "36K Python contest problems", 2.7),
    Source("livecodebench", "competitive", "hf", "bzantium/livecodebench", "reference",
           "Recent contest problems with test cases. CC", 4.5),

    # --- System design ---
    Source("system-design-primer", "system_design", "git", "donnemartin/system-design-primer", "cards",
           "Canonical system design guide + solved scenarios", 0.01),
    Source("system-design-karan", "system_design", "git", "karanpratapsingh/system-design", "cards",
           "Full system design course in markdown", 0.01),
    Source("system-design-101", "system_design", "git", "ByteByteGoHq/system-design-101", "reference",
           "ByteByteGo visual explainers", 0.05),
    Source("awesome-system-design", "system_design", "git", "ashishps1/awesome-system-design-resources", "reference",
           "Concept list + links. GPL-3.0", 0.0),
    Source("grokking-system-design", "system_design", "git", "Jeevan-kumar-Raj/Grokking-System-Design", "reference",
           "Grokking-style case studies. GPL-3.0", 0.0),
    Source("awesome-scalability", "system_design", "git", "binhnguyennus/awesome-scalability", "reference",
           "Real-world scalability articles (links). MIT", 0.0),
    Source("system-design-interview-checkcheckzz", "system_design", "git", "checkcheckzz/system-design-interview",
           "reference", "Company system design questions + links", 0.0),

    # --- LLD / OOD ---
    Source("grokking-ood", "lld", "git", "tssovi/grokking-the-object-oriented-design-interview", "reference",
           "OOD case studies: parking lot, library, etc.", 0.01),
    Source("awesome-lld", "lld", "git", "ashishps1/awesome-low-level-design", "reference",
           "LLD problems with code in several languages. GPL-3.0", 0.02),

    # --- CS fundamentals ---
    Source("ostep", "cs", "url_index", "https://pages.cs.wisc.edu/~remzi/OSTEP/", "cards",
           "Operating Systems: Three Easy Pieces, 68 chapter PDFs", 0.05),
    Source("little-book-of-semaphores", "cs", "url",
           "https://greenteapress.com/semaphores/LittleBookOfSemaphores.pdf", "reference",
           "Concurrency problems", 0.0),
    Source("last-minute-notes", "cs", "git", "anxkhn/LastMinuteNotes", "reference",
           "CN, DBMS/SQL, OOP, OS notes", 0.07),
    Source("cs-fundamentals-interview", "cs", "git", "JayrajSinh16/CS-Fundamentals-Interview", "reference",
           "CS fundamentals interview Q&A", 0.0),
    Source("devops-exercises", "cs", "git", "bregman-arie/devops-exercises", "reference",
           "Q&A on Linux, networking, databases, Docker, Kubernetes", 0.01),
    Source("computer-networking", "cs", "git", "bregman-arie/computer-networking", "reference",
           "Networking resources. Apache-2.0", 0.0),
    Source("java-basics", "cs", "git", "learning-zone/java-basics", "reference",
           "Java Q&A (Java 25)", 0.12),
    Source("java-interview-guide", "cs", "git", "in28minutes/interview-guide", "reference",
           "200+ Java Q&A", 0.0),
    Source("java-interview-devinterview", "cs", "git", "Devinterview-io/java-interview-questions", "reference",
           "Java Q&A", 0.0),
    Source("sql-basics", "cs", "git", "learning-zone/sql-basics", "reference",
           "SQL Q&A", 0.0),

    # --- AI / ML ---
    Source("aiml-interviews", "ai", "git", "alirezadir/AIMLInterviews", "reference",
           "ML/AI interview guide. MIT", 0.01),
    Source("ml-interviews-book", "ai", "git", "chiphuyen/ml-interviews-book", "reference",
           "Chip Huyen's ML interviews book", 0.01),
    Source("llm-interview-questions", "ai", "git", "llmgenai/LLMInterviewQuestions", "reference",
           "LLM interview questions", 0.0),
    Source("data-science-interview", "ai", "git", "youssefHosni/Data-Science-Interview-Questions-Answers",
           "reference", "Data science Q&A", 0.0),

    # --- General / behavioral ---
    Source("tech-interview-handbook", "behavioral", "git", "yangshun/tech-interview-handbook", "reference",
           "Behavioral questions, interview process, algorithm cheatsheets. MIT", 0.03),
    Source("coding-interview-university", "behavioral", "git", "jwasham/coding-interview-university", "reference",
           "CS study plan. CC-BY-SA-4.0", 0.02),
    Source("big-companies-interview-questions", "behavioral", "git", "realabbas/big-companies-interview-questions",
           "reference", "Questions asked at big companies. CC0", 0.0),
    Source("kdn251-interviews", "behavioral", "git", "kdn251/interviews", "reference",
           "Interview prep collection. MIT", 0.02),

    # --- Structure sources (private corpus only; see .planning/content-rebuild.md) ---
    # Neither is rendered to users. They seed lesson generation and the vector
    # index, and their real value is structure: what a domain must cover, and
    # what real interviews actually ask.
    Source("roadmap-sh", "system_design", "git", "kamranahmedse/developer-roadmap", "reference",
           "One short authoritative definition per roadmap node, plus the node ordering. "
           "Copyright nilbuild (was kamranahmedse), personal use only - never rendered to users. "
           "10,899 node files across 94 roadmaps; sparse-checkout keeps the text and drops the "
           "repo's own tooling.", 0.04,
           paths=("roadmaps/*/content/",)),
    Source("systemdesign-io", "system_design", "url_links", "https://systemdesign.io/", "reference",
           "55 system design questions from real interviews: difficulty, company tags and the "
           "follow-ups an interviewer probes with. No solutions - the site is still writing them.",
           0.01, link_pattern=r"/question/[a-z0-9-]+"),
]
