import os

# CHUNKING PARAMS
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 50
TOP_K = int(os.environ.get("TOP_K", 4))

# Chroma persist directory
CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR")

# DB: keep for metadata (optional). If you use Postgres set DATABASE_URL accordingly.
DATABASE_URL = os.environ.get("DATABASE_URL")


GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL = os.environ.get("GROQ_MODEL")

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")