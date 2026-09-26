from pathlib import Path

from dotenv import load_dotenv

PIPELINE_DIR = Path(__file__).resolve().parents[2]
REPO_DIR = PIPELINE_DIR.parent
DATA_DIR = REPO_DIR / ".data"

# HF_TOKEN, ANTHROPIC_API_KEY, DATABASE_URL
load_dotenv(PIPELINE_DIR / ".env")
