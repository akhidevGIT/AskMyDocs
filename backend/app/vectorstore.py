from langchain_chroma import Chroma
from .embeddings import get_embeddings
from .config import CHROMA_PERSIST_DIR



def get_vectorstore():
    embeddings = get_embeddings()
    vectordb = Chroma(collection_name="my_collection_mpnet",
                      embedding_function=embeddings,
                      persist_directory=CHROMA_PERSIST_DIR)
    return vectordb

def persist_vectorstore(vectordb):
    # Chroma persists automatically if persist_directory provided, but call persist() to be safe
    try:
        vectordb.persist()
    except Exception:
        pass