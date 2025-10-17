from .config import GROQ_API_KEY, GROQ_MODEL
from langchain.prompts import PromptTemplate

from langchain_groq import ChatGroq

from pydantic import BaseModel
from .config import TOP_K
from fastapi import APIRouter
from .vectorstore import get_vectorstore

router = APIRouter(prefix="/query", tags=['query'])


class QueryRequest(BaseModel):
    query: str
    top_k: int = TOP_K



@router.post("/search")
def search_and_answer(req: QueryRequest):
    vectordb = get_vectorstore()
    docs = vectordb.similarity_search(req.query, k= req.top_k)
     # docs is list of langchain Documents objects with .page_content and .metadata
    if not docs:
        return {"answer": "No relevant documents found.", "sources": []}
    # Deduplicate by text
    unique_texts = []
    unique_docs = []
    for d in docs:
        if d.page_content not in unique_texts:
            unique_texts.append(d.page_content)
            unique_docs.append(d)
    docs = unique_docs[:req.top_k]

    # Build context string (simple concatenation). Trim if necessary.
    snippets = []
    sources = []
    for d in docs:
        snippet = d.page_content
        meta = d.metadata or {}
        src = meta.get("source", "unknown")
        idx = meta.get("chunk_index", None)
        label = f"{src} [{idx}]" if idx is not None else src
        snippets.append(f"---\nSource: {label}\n{snippet}\n")
        if label not in sources:
            sources.append(label)

    context = "\n\n".join(snippets)

    # If GROQ key available, call LLM via LangChain ChatGroq wrapper
    if GROQ_API_KEY:
        system = (
            "You are an assistant that must answer using only the provided context. "
            "If the answer is not contained in the context, say you don't know. "
            "Be concise and include a 'Sources:' line listing the sources you used."
        )

        prompt_template = """{system}

                        CONTEXT:
                        {context}

                        USER QUESTION:
                        {question}
                        Answer concisely. Just the concise answer for the query would be enough no need to add sources."""
        
        prompt = PromptTemplate(input_variables=["system", "context", "question"], template=prompt_template)
        llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY)
        chain = prompt | llm 
        answer = chain.invoke({"system": system, "context": context, "question": req.query})
        return {"answer": answer.content, "sources": sources, "raw_retrieved": [d.page_content for d in docs]}
    else:
        # Fallback: return concatenated context as answer (no LLM)
        preview = context[:2000] + ("..." if len(context) > 2000 else "")
        return {"answer": f"(LLM disabled) Retrieved context:\n\n{preview}", "sources": sources}







