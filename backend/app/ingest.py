import os

from fastapi import UploadFile, File, HTTPException, APIRouter
import tempfile
from .vectorstore import get_vectorstore, persist_vectorstore
from .process_docs import text_extraction_from_docs
from .chunking import chunk_documents
from uuid import uuid4


router = APIRouter(prefix="/ingest", tags=['data_ingest'])



@router.post("/")
async def ingest_file(upload_file: UploadFile = File(...), title: str = "", description: str = ""):
    if not upload_file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    raw_filepath = upload_file.filename
    root, extension = os.path.splitext(raw_filepath)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix= extension) as tmp_file:
        content = await upload_file.read()
        tmp_file.write(content)

        tmp_file.flush()

        # Get the path to the temporary file
        temp_file_path = tmp_file.name

    documents = text_extraction_from_docs(temp_file_path)
    chunks = chunk_documents(documents)
    
    if len(chunks) == 0:
        raise HTTPException(status_code=400, detail="No text extracted from document.")
    # Add metadata to each chunk
    for chunk in chunks:
        chunk.metadata = {
            "source": upload_file.filename,
            "chunk_index": str(uuid4())
        }
    vectordb = get_vectorstore()
    vectordb.add_documents(documents=chunks)
    persist_vectorstore(vectordb)


    return {"filename": upload_file.filename, "num_chunks": len(chunks)}