import streamlit as st
import requests
import os
# -------------------------------
# Configuration
# -------------------------------
st.set_page_config(page_title="AskMyDocs", page_icon="📚", layout="wide")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# -------------------------------
# Session state setup
# -------------------------------
if "ingested" not in st.session_state:
    st.session_state.ingested = False
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# -------------------------------
# Header
# -------------------------------
st.title("📚 AskMyDocs — RAG-powered Knowledge Chatbot")
st.write("Upload your documents (PDF, DOCX, TXT) and ask questions based on their contents.")

# -------------------------------
# File upload & ingestion
# -------------------------------
st.subheader("Upload Documents")
with st.form("upload_form", clear_on_submit=True):
    uploaded_file = st.file_uploader("Select a document", type=["pdf", "docx", "txt"])
    title = st.text_input("Title (optional)")
    description = st.text_area("Description (optional)")
    submitted = st.form_submit_button("Ingest Document")

    if submitted:
        if not uploaded_file:
            st.warning("⚠️ Please select a file to upload.")
        else:
            with st.spinner("📥 Uploading and ingesting document..."):
                files = {"upload_file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {"title": title or uploaded_file.name, "description": description or ""}
                try:
                    res = requests.post(f"{API_URL}/ingest", files=files, data=data)
                    if res.status_code == 200:
                        info = res.json()
                        st.success(f"✅ Ingested `{uploaded_file.name}` successfully — {info.get('num_chunks', '?')} chunks added.")
                        st.session_state.ingested = True
                        st.session_state.uploaded_files.append(uploaded_file.name)
                    else:
                        st.error(f"❌ Ingestion failed: {res.text}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")

# -------------------------------
# Query area (visible only after ingestion)
# -------------------------------
if st.session_state.ingested:
    st.markdown("---")
    st.subheader("💬 Ask a question about your documents")

    query = st.text_input("Enter your question:")
    top_k = st.number_input("Top K results to retrieve", min_value=1, max_value=10, value=4, step=1)

    if st.button("🔍 Search"):
        if not query.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking... retrieving and generating answer..."):
                payload = {"query": query, "top_k": int(top_k)}
                try:
                    res = requests.post(f"{API_URL}/query/search", json=payload)
                    if res.status_code == 200:
                        data = res.json()

                        # Save to session state so it persists across reruns
                        st.session_state.last_answer = data.get("answer")
                        st.session_state.last_sources = data.get("sources", [])
                        st.session_state.last_chunks = data.get("raw_retrieved", [])

                    else:
                        st.error(f"Query failed: {res.text}")
                except Exception as e:
                    st.error(f"Error querying backend: {e}")

    # Display the last result if available
    if "last_answer" in st.session_state:
        st.markdown("### 🧠 Answer")
        st.write(st.session_state.last_answer)

        if st.session_state.last_sources:
            st.markdown("**Sources:**")
            for s in st.session_state.last_sources:
                st.write(f"- {s}")

        if st.checkbox("Show retrieved document chunks"):
            for i, doc in enumerate(st.session_state.last_chunks):
                st.markdown(f"**Chunk {i+1}:**")
                st.code(doc[:1000] + ("..." if len(doc) > 1000 else ""))
else:
    st.info("⬆️ Please upload and ingest at least one document to start asking questions.")

# -------------------------------
# Sidebar summary
# -------------------------------
st.sidebar.header("📄 Uploaded Files")
if st.session_state.uploaded_files:
    for f in st.session_state.uploaded_files:
        st.sidebar.write(f"- {f}")
else:
    st.sidebar.write("No files uploaded yet.")
