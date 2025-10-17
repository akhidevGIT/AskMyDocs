from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader



def text_extraction_from_docs(file_path:str):

    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    else:
        return {"error": "Unsupported file type",
                "filename": file_path }
    
    documents = loader.load()
    
    return documents


    
