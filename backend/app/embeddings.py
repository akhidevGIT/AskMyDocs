# Wrapper to produce embeddings using sentence-transformers
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from .config import EMBEDDING_MODEL

def get_embeddings():
    # uses 'all-MiniLM-L6-v2' by default
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return embeddings
