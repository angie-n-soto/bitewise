import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Gemini API Key (required for Google Antigravity SDK)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# The model to use for the agents
# Gemini 2.5 Flash is recommended, but we can default to gemini-2.5-flash or use others.
AGENT_MODEL = os.getenv("AGENT_MODEL", "gemini-2.5-flash")

# Verify configuration on load
if not GEMINI_API_KEY:
    print("[WARNING] GEMINI_API_KEY environment variable is not set. Please set it in your environment or a .env file.")
