# Executive Summary  
We propose building **90X** as a “90‑day interview training OS” that ingests open-source interview data and tracks user progress. Key steps include cataloging open-source DSA and design problem sets, defining a normalized schema, and writing ingestion scripts to pull in those resources. For DSA we’ll leverage Hugging Face datasets and GitHub repos (e.g. LeetCode/Codeforces problem dumps), and for system design/LLD use open guides (e.g. the System Design Primer and Grokking OOD). We outline specific sources with URLs and licenses, design SQL schemas (Problems, SystemDesign, etc.), and an ingestion pipeline (shown in a Mermaid flowchart). We distinguish fully automated pulls (HF datasets, Git clones) from manual steps (sanity-checking scraped content). A minimal v1 seed list (e.g. AllenHung’s LeetCode, PrimeIntellect’s coding dataset, DonneMartin’s System Design Primer) is given with rationale. Finally we sketch AI-enrichment tasks (e.g. pattern tagging via LLMs) and note local-only usage and license concerns.  

## 1. Open-Source Data Catalog  
We need datasets covering **coding problems (DSA)**, **system design/HLD scenarios**, **OOD/LLD examples**, and some **CS fundamentals**. Below is a prioritized list of sources, with links and license notes:

| Category              | Source (URL)                                                   | License          | Notes / Size                          |
|-----------------------|----------------------------------------------------------------|------------------|---------------------------------------|
| **DSA – LeetCode problems**      | HF: allenhung1025/**leetcode**       | (likely Apache 2.0 on HF) | ~2.6K problems; includes title, statement, difficulty, and code solutions in Java/C++/Python. Good breadth of common problems. (HF dataset) |
| **DSA – Mixed problems**         | HF: xtremekiwi/**APPS-leetcode-codeforces** | MIT              | ~250 LeetCode/Codeforces problems (train split) with Python solutions and I/O examples. Useful as sample set (license MIT). |
| **DSA – Verifiable problems**    | HF: PrimeIntellect/**verifiable-coding-problems**    | (unspecified on HF, likely public) | ~144K coding problems with prompts and “gold” Python/C++ solutions from coding contests (lots of Codeforces tasks with I/O tests). Very large coverage. |
| **DSA – Python coding**         | HF: open-r1/**verifiable-coding-problems-python**     | (as above)       | ~36K Python-specific problems (verifiable code). Overlaps with PrimeIntellect. Good for variety of patterns. |
| **DSA – Competitive (CF)**      | HF: bzantium/**livecodebench**    | CC (CC-BY likely) | ~1K recent Codeforces problems (2023-2025) with statements, sample tests, and code. Easy/medium/hard mix, licensed CC. |
| **Interview Q’s (curated)**     | GitHub: ombharatiya/**FAANG-Coding-Interview-Questions** | GPL-3.0         | Curated collection of coding, system design, ML questions across FAANG-like companies (2025–2026). Contains markdown lists of Top 75/Blind 75 problems and company-specific Q’s (license GPL). |
| **System Design Scenarios**     | GitHub: donnemartin/**system-design-primer**    | MIT              | Open guide to designing scalable systems. Includes canonical interview questions (Pastebin, Twitter feed, web crawler, etc.) with solution outlines. Well-structured Markdown. |
| **OOD/LLD Case Studies**        | GitHub: tssovi/**grokking-oo-design-interview**  | MIT (?)         | Extended “Grokking” repo covering OOP design case studies: Library system, Parking lot, E-commerce, etc. Contains UML diagrams and Python pseudocode. |
| **CS Fundamentals – OS**        | “OSTEP” Operating Systems text (Arpaci-Dusseau, MIT Open)        | Creative Commons | Full textbook on OS topics (threads, memory, file systems). We can extract key concepts/quizzes from chapters. |
| **CS Fundamentals – Concurrency** | “Little Book of Semaphores” (Allen Downey)                        | CC BY          | Classic concurrency problems and solutions (C/Python code). Good exercises in multithreading/races. |
| **CS Fundamentals – DB/SQL**     | (none standard – potential to add SQLZoo or similar)             | —                | Possibly use existing tutorials/quizzes (no widely-known open database book with exercises; skip for v1). |
| **Networking/Systems**         | (Cover basics via open lecture notes/Cookbook: e.g. Kurose/Cambridge slides) | —       | Could scrape key networking FAQs or slides (low priority for v1). |
| **Behavioral prompts**        | (Self-curated list of STAR interview questions)                   | —                | No open dataset; we’ll manually list common questions (e.g. leadership stories). |

*Quality:* Most HF datasets have clean structured data (JSON/Parquet). GitHub repos are maintained by communities (system-design-primer is up-to-date and MIT-licensed). We should **avoid proprietary content** (e.g. don’t scrape LeetCode/GFG web pages). All listed sources above are public/open.

## 2. 90X Content Schema  
We define a relational schema (e.g. PostgreSQL) to normalize content. Key tables (shown below) include `dsa_problems`, `system_design`, `lld_problems`, and a `concepts` table for CS fundamentals. Fields capture provenance, difficulty, tags, and solutions. Example SQL:

```sql
-- Table for algorithmic problems
CREATE TABLE dsa_problems (
    id SERIAL PRIMARY KEY,
    slug TEXT,               -- e.g. "two-sum"
    title TEXT,
    description TEXT,
    difficulty TEXT,         -- e.g. 'Easy','Medium','Hard'
    topics TEXT[],           -- e.g. ['array','hashmap']
    pattern TEXT,            -- e.g. 'two pointers', identified later by AI
    source_url TEXT,         -- original URL or dataset link
    license TEXT,            -- e.g. 'MIT'
    solution_code TEXT,      -- canonical solution snippet or link
    solution_lang TEXT,      -- language of solution (if code)
    test_cases JSONB         -- example I/O in JSON
);
-- Table for system-design tasks
CREATE TABLE system_design (
    id SERIAL PRIMARY KEY,
    name TEXT,               -- e.g. 'Design Pastebin'
    description TEXT,        -- problem statement / prompt
    requirements TEXT,       -- extracted use-cases/constraints
    solution_outline TEXT,   -- HLD description or notes
    rubric JSONB,            -- e.g. scores for categories (scalability, tradeoffs, etc.)
    difficulty TEXT,         -- subjective difficulty/level
    source_url TEXT,
    license TEXT
);
-- Table for object-oriented design / LLD problems
CREATE TABLE lld_problems (
    id SERIAL PRIMARY KEY,
    title TEXT,              -- e.g. 'Parking Lot Design'
    description TEXT,
    class_diagram TEXT,      -- maybe PlantUML code or image URL
    code_examples TEXT,      -- code stubs or examples
    key_concepts TEXT[],
    source_url TEXT,
    license TEXT
);
-- Table for CS fundamental concepts/quizzes
CREATE TABLE concepts (
    id SERIAL PRIMARY KEY,
    category TEXT,           -- e.g. 'Operating Systems', 'Concurrency', 'SQL'
    topic TEXT,              -- e.g. 'Paging', 'Semaphore', 'Indexes'
    description TEXT,        -- explanatory notes or question
    key_points TEXT[],       -- bullet-point answers or facts
    references JSONB,        -- URLs or book references
    source_url TEXT,
    license TEXT
);
```

We’ll also store **user practice data**. For example:

```sql
CREATE TABLE user_attempts (
    attempt_id SERIAL PRIMARY KEY,
    user_id TEXT,            -- e.g. 90X user identifier
    problem_id INT REFERENCES dsa_problems(id),
    attempt_time TIMESTAMP,
    time_sec INT,
    solved BOOLEAN,
    hints_used INT,
    mistakes TEXT[],         -- e.g. ['did not recognize sliding-window']
    notes TEXT
);
```

This schema is normalized (no redundancy) and captures all needed fields (source attribution, tags, user performance). Additional tables (e.g. for mock interview transcripts) can be added similarly.

## 3. Ingestion Pipeline & Script  

Below is a high-level flowchart of the ingestion process, followed by an outline of a combined bash/Python script to fetch and normalize data:

```mermaid
flowchart TD
    A[HuggingFace Datasets] -->|via `datasets` or `hf` CLI| B[Raw JSON/Parquet files]
    C[GitHub Repos (DSA/Design)] -->|git clone| D[Local files (MD/IPynb/CSV)]
    B & D --> E[Parser/Normalizer Script]
    E --> F[Insert into 90X Postgres DB]
    E --> G[Generate JSON files per table (for dev)]
    style A fill:#f9f,stroke:#333,stroke-width:1px
    style C fill:#ff9,stroke:#333,stroke-width:1px
    style E fill:#9fc,stroke:#333,stroke-width:1px
    style F fill:#cff,stroke:#333,stroke-width:1px
    style G fill:#fcf,stroke:#333,stroke-width:1px
```

**Example ingestion steps (v1):** (in pseudocode/batch form)

```bash
#!/bin/bash
# 1. Prepare directories
mkdir -p 90x/data/{dsa,system_design,lld,concepts}

# 2. Clone GitHub sources
git clone https://github.com/donnemartin/system-design-primer.git 90x/data/system_design/system-design-primer
git clone https://github.com/ombharatiya/FAANG-Coding-Interview-Questions.git 90x/data/dsa/faang-questions
git clone https://github.com/tssovi/grokking-the-object-oriented-design-interview.git 90x/data/lld/grokking-ood

# 3. Download HuggingFace datasets via Python
python3 << 'EOF'
from datasets import load_dataset
# DSA problems
ds1 = load_dataset("allenhung1025/leetcode", split="train")
ds1.to_parquet("90x/data/dsa/allenhung_leetcode.parquet")
ds2 = load_dataset("xtremekiwi/APPS-leetcode-codeforces", split="train")
ds2.to_parquet("90x/data/dsa/apps_coding.parquet")
ds3 = load_dataset("PrimeIntellect/verifiable-coding-problems", split="train")
ds3.to_parquet("90x/data/dsa/primeintellect.parquet")
ds4 = load_dataset("open-r1/verifiable-coding-problems-python", split="train")
ds4.to_parquet("90x/data/dsa/verifiable_python.parquet")
ds5 = load_dataset("bzantium/livecodebench", split="test")
ds5.to_parquet("90x/data/dsa/livecodebench.parquet")
EOF
```

```bash
# 4. Normalize & insert (Python)
python3 scripts/ingest.py
```

In **`ingest.py`**, we would parse each source, extract relevant fields, dedupe (e.g. by slug or unique ID), and insert into our DB (using psycopg or SQLAlchemy). For example:

```python
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect("dbname=90x user=...")

def ingest_dsa():
    # Example: load AllenHung parquet
    df = pd.read_parquet("90x/data/dsa/allenhung_leetcode.parquet")
    for _, row in df.iterrows():
        # Extract fields (slug, title, etc.)
        # Insert into dsa_problems
        # ...
        pass

# ... similar for other datasets ...

def ingest_system_design():
    # Walk through system-design-primer solutions folder
    import glob, frontmatter
    for mdfile in glob.glob("90x/data/system_design/system-design-primer/solutions/system_design/*/README.md"):
        text = open(mdfile).read()
        # Use YAML frontmatter or regex to split out question vs solution
        # Example: first heading is question, rest is solution steps.
        # Insert into system_design table.
        pass

# Finally run each
ingest_dsa()
ingest_system_design()
```

This script would include error handling (skip missing fields, log conflicts). It can **dedupe** by checking if a slug or URL already exists.

## 4. Manual vs Automated Ingestion  

| Source                                | Ingestion Method     | Manual Review Needed? | Comments                         |
|---------------------------------------|----------------------|-----------------------|----------------------------------|
| Hugging Face Parquet/JSON (e.g. allenhung1025/leetcode) | Automated via `datasets.load_dataset` → CSV/Parquet → Python parse | No (structured) | Data is well-formatted. We should verify no duplicates (Slug collisions). |
| GH Repo (system-design-primer) – MD    | Automated script parsing Markdown sections | Light (validate parsing) | The Markdown is structured (sections), but verify that scraping headings works. |
| GH Repo (grokking-ood) – MD/IPynb      | Mostly automated (parse Markdown for prompts/solutions) | Medium (check formatting) | Some content is in Jupyter notebooks (may skip code), mostly text. Requires checking diagrams. |
| GH Repo (FAANG-questions) – MD         | Automated parse (extract lists of questions) | Light | Content is in markdown lists. Ensure license compliance (GPL) – use only locally. |
| OSTEP book (PDF/HTML)                 | Manual/partial (extract key Q’s)      | Yes | Need to pick representative concepts. Likely manual extraction or PDF reading. |
| Little Book of Semaphores (online)     | Manual summarization or OCR            | Yes | Could manually transcribe a few semaphore exercises. |
| Behavioral Q’s (no dataset)           | Manual curation                     | Yes | Write own list of 10–20 common prompts (no license issue). |

**Automated:** HuggingFace datasets and Git clones are fetched by scripts. **Manual review:** Needed for any scraped content or converted text (e.g. verifying OSTEP chapter sections, confirming license). Behavior questions will be authored in-house.

## 5. V1 Seed Dataset List  

As a minimal seed, we’d immediately pull the following (10–15 sources) because they cover core DSA and design content:

| Source (URL)                                    | Why (Coverage/Quality)                |
|-------------------------------------------------|---------------------------------------|
| **allenhung1025/leetcode (HuggingFace)**   | 2,600 curated LeetCode problems with solution code. Covers arrays, strings, etc.     |
| **xtremekiwi/APPS-leetcode-codeforces**   | ~250 mixed LeetCode/Codeforces problems (with Python solutions & testcases). Quick start set. (MIT-licensed) |
| **PrimeIntellect/verifiable-coding-problems** | 144K+ competitive programming problems (CF + others) with "gold" solutions. Ensures huge breadth of patterns. |
| **open-r1/verifiable-coding-problems-python**     | 35K+ Python-specific problem prompts. Good for Python practice and textual variety. |
| **bzantium/livecodebench**                      | 1K recent Codeforces problems (2023-2025). Ensures up-to-date practice across easy to hard. (CC license) |
| **donnemartin/system-design-primer**         | Canonical system design Qs (Pastebin, Twitter feed, web crawler, etc.) with structured solutions. (MIT license) |
| **tssovi/grokking-oo-design-interview**     | 20+ OOD case studies (Parking Lot, Library, Shopping, etc.) with UML and code templates. (Likely MIT license) |
| **FAANG-Coding-Interview-Questions**       | Curated list of 75+ essential coding problems (Blind 75, company Q’s). Helps seed question patterns. (GPL license – use locally) |
| **Little Book of Semaphores (Downey)**                 | Classic concurrency puzzles. Good for threading concept practice. (CC license) |
| **OSTEP (Operating Systems)**                         | Key OS concepts (threads, VM, files) – good for quizzes/flashcards. (CC license) |
| **Any Top LeetCode Lists (Blind-75/NeetCode)**        | Built-in or scraped lists (as text) to identify must-know problems. (Use only as guide, not data) |

This seed list focuses on **DSA** and **system design**. We omit heavier integration (like full site scraping) initially. Each source is open or free for personal use. The license notes above are considered: for GPL sources (FAANG), we only use locally.

## 6. AI Enrichment Plan  

Once raw data is ingested, we’ll enrich it via AI/ML:

- **Tagging & Patterns:** Use a language model (e.g. OpenAI GPT or a local model) to label each DSA problem with topics and problem patterns (two-pointers, DP, graph, etc.). E.g., prompt the question text: “What algorithmic pattern does this problem use?” and store in `pattern`.  
- **Difficulty Calibration:** Normalize difficulty labels (Easy/Medium/Hard) across sources. Possibly train a small classifier on known examples.  
- **Summaries/Rubrics:** For system-design scenarios, parse solutions to extract key sections (requirements, bottlenecks, trade-offs) into the `rubric` JSON. LLM can split a solution text into bullet points under "Latency", "Scalability", etc.  
- **Semantic Search Index:** Compute text embeddings (e.g. via OpenAI Embeddings or Sentence-BERT) for all questions and solutions. Build a vector index (e.g. via FAISS or Elastic Vector) so the AI coach can quickly find similar problems or relevant design topics.  
- **Mistake Analysis:** For logged user attempts, use AI to categorize mistakes (e.g. “misidentified pattern” vs “logic bug”). Possibly fine-tune a model on common error types.  
- **Chat/Feedback Bot:** Ultimately integrate an AI tutor (fine-tuned GPT or Claude) that can ask follow-ups for system-design (as in [22]) and provide hints. It would consume rubric and ask domain-specific questions (e.g. “Why choose NoSQL?”).

Tools: Hugging Face Transformers, OpenAI API (e.g. gpt-4o for analysis), LangChain for orchestration. We may run lighter models locally for tag inference to keep latency low.

## 7. Security & Legal Considerations  

- **Licenses:** All data will be stored locally for personal training use. We **must respect licenses**:
  - MIT/Apache/CC-licensed content (System Design Primer, Grokking OOD, LBOS, OSTEP) is free to use with attribution.  
  - GPL-licensed sources (FAANG Qs) are okay for private use, but cannot be redistributed or included in any product. (Flag: use only offline).  
  - Hugging Face data is usually under permissive terms, but we include license metadata in our DB schema to audit reuse.
- **Copyright:** We avoid scraping copyrighted tutorial sites. We rely only on explicitly open data.  
- **Privacy:** As this is local and user-specific, no personal data issues. However, user attempts data should be secured (it belongs to the user).
- **Security:** The ingestion scripts should validate/escape any code content (no auto-execute dangerous code from datasets). Test cases or solutions will be stored as text only.

## 8. Deliverables & Runbook  

**Repository Structure (90x/):**

- `90x/data/` – Raw ingested files (parquet, markdown, etc.)  
- `90x/scripts/ingest.py` – Python script to load/normalize and insert into DB.  
- `90x/schemas/` – SQL DDL (schema.sql) and/or JSON schema definitions.  
- `README.md` – Overview and usage instructions.  
- `runbook.md` – One-line commands for ingestion.  
- `sample_output/` – Example JSON or CSV exports of tables (for verification).

**Key Files:**

- **`schemas/schema.sql`** – contains the `CREATE TABLE` statements from Section 2.  
- **`scripts/ingest.py`** – script with functions: `ingest_dsa()`, `ingest_system_design()`, etc.  
- **`runbook.md`** – lists commands to set up environment, pull data, run ingestion.

**Runbook (commands):**  

```bash
# (from repository root)
# 1. Install Python deps
pip install datasets psycopg2 pandas

# 2. Clone data repos
bash 90x/scripts/fetch_repos.sh    # contains all git clone commands

# 3. Download HF datasets
bash 90x/scripts/download_hf.sh   # uses datasets.load_dataset, see section 3

# 4. Initialize database
psql 90x_db -f 90x/schemas/schema.sql

# 5. Run ingestion
python3 90x/scripts/ingest.py

# 6. Verify (export sample)
psql 90x_db -c "SELECT slug, difficulty FROM dsa_problems LIMIT 5;" > sample_output/dsa_sample.txt
```

This setup will pull in initial data and load it into the 90X DB. Further steps (AI enrichment, dashboard, UI) will build on this foundation.

**Sources:** The data sources and workflows above are drawn from public repositories and dataset descriptions. 

