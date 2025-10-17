# 🧠 AskMyDocs — RAG-powered Knowledge Chatbot

**AskMyDocs** is an end-to-end **Retrieval-Augmented Generation (RAG)** application built for personalized document-based question answering. Upload your PDFs, ask natural-language questions, and get AI-generated answers *grounded in your own data*.

---

## Key Features

- **PDF Upload & Processing** — Ingest your own documents  
- **RAG Pipeline** — Retrieve relevant chunks & generate context-aware answers  
- **LangChain Integration** — Modular document loaders, text splitters, retrievers, and LLM chain  
- **Groq LLM API** — Ultra-fast inference with `llama3` model (Groq free tier)  
- **Streamlit UI** — Simple, clean interface for chat-based document Q&A  
- **Feedback Loop** — Collect user ratings and comments on AI responses  
- **PostgreSQL Support** — Store feedback and metadata  
- **Dockerized Deployment** — Easy to run locally or on Streamlit Cloud

---


---

## Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit |
| **Backend** | FastAPI |
| **Vector DB** | Chroma |
| **LLM API** | Groq (`llama3`) |
| **Framework** | LangChain |
| **Database** | PostgreSQL |
| **Deployment** | Docker + Streamlit Cloud |

---

## 🧠 How It Works

1. **Upload** your document(s) in Streamlit.  
2. The backend splits text into chunks and creates vector embeddings.  
3. **User query** is matched with the most relevant chunks using Chroma.  
4. The **Groq LLM** generates a contextual answer using retrieved data.  
5. User can give **feedback** (👍 / 👎 + comment).  
6. Feedback data is stored for continuous improvement.

---

## 🧰 Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/akhidevGIT/AskMyDocs.git
cd AskMyDocs
```
### 2️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # (Mac/Linux)
venv\Scripts\activate     # (Windows)
```
### 3️⃣ Create a .env file

At the project root (same folder as docker-compose.yml), create .env and set these variables :
```
CHROMA_PERSIST_DIR = ../data/chromadb
DATABASE_URL = postgresql://<username>:<password>@<host>:<port>/<databasename>
TOP_K = top_k_chunks_for_context
GROQ_API_KEY = your_groq_api_key
GROQ_MODEL = llama-3.3-70b-versatile
EMBEDDING_MODEL = sentence-transformers/all-mpnet-base-v2

```
### 4️⃣ Run Locally with Docker Compose
Build and start all containers (backend, frontend):
```bash
docker compose up --build
```
3️⃣ Open in browser:

**Frontend (Streamlit)**: http://localhost:8501

**Backend Docs (FastAPI)**: http://localhost:8000/docs


## Demo (Sample Flow)

1. Upload a document
2. Wait for ingestion success ✅
3. Ask: “Summarize the key points from the report”
4. Get AI response 💬
5. Give feedback 👍/👎

## 📚 Learning Highlights

This project demonstrates:

- Building a RAG pipeline using LangChain
- Integrating Groq API for LLM inference
- Connecting FastAPI backend ↔ Streamlit frontend
- Managing state and feedback data persistence
- Deploying on Docker + Streamlit Cloud

## Future Enhancements

- Multi-file ingestion
- Semantic search over all documents
- Admin analytics dashboard
- Feedback-based fine-tuning of LLM

## 🧑‍💻 Author

Akhila Devarapalli
Data Scientist | GenAI Enthusiast








