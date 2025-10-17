from .config import CHUNK_OVERLAP, CHUNK_SIZE
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents, chunk_size:int = CHUNK_SIZE, chunk_overlap:int = CHUNK_OVERLAP):
    text_Splitter = RecursiveCharacterTextSplitter(chunk_size= chunk_size,
                                                   chunk_overlap = chunk_overlap,
                                                   length_function = len)
    chunks = text_Splitter.split_documents(documents)
    
    return chunks


