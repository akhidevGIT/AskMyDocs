from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import ingest, query_answer_llm
from . import config
import os

# Create DB tables
#db.Base.metadata.create_all(bind=db.engine)

app = FastAPI(title="AskMyDocs - RAG backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # limit in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(query_answer_llm.router)

