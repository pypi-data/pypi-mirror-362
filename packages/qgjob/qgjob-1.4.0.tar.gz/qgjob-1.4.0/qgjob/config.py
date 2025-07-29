import os

# Allow override by env var
API_BASE_URL = os.environ.get("QGJOB_API_BASE_URL", "http://localhost:8000")
