from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_PATH = os.getenv("DB_PATH", "prompts_db.sqlite")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")