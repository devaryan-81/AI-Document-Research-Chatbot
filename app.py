import streamlit as st
import requests
import pandas as pd
import uuid

API = "http://localhost:8000"

st.set_page_config(page_title="Document Research Chatbot", layout="wide")

# ---------- Session State ----------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

st.title("📄 Agentic Document Research Chatbot")

# ---------- Backend health check ----------
def check_backend():
    try:
        r = requests.get(f"{API}/health", timeout=3)
        return r.status_code == 200, r.json()
    except requests.exceptions.ConnectionError:
        return False, None

healthy, health_data = check_backend()
if not healthy:
    st.error(f"⚠️ Backend not reachable at {API}. Start it with: `uvicorn main:app --reload --port 8000`")
    st.stop()
else:
    st.success(f"Backend connected — {health_data.get('indexed_chunks', 0)} chunks indexed")

st.divider()

# ---------- 1. Upload ----------
st.header("1. Upload Documents")

col_a, col_b = st.columns([3, 1])
with col_a:
    uploaded_files = st.file_uploader(
        "Upload PDFs/Images (multiple allowed)",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )
with col_b:
    author = st.text_input("Author (optional)")

if st.button("Upload All", type="primary") and uploaded_files:
    progress = st.progress(0, text="Uploading...")
    results = []
    for i, f in enumerate(uploaded_files):
        try:
            files = {"file": (f.name, f.getvalue())}
            data = {"author": author} if author else {}
            r = requests.post(f"{API}/upload", files=files, data=data, timeout=120)
            r.raise_for_status()
            results.append(r.json())
        except Exception as e:
            st.error(f"Failed to upload {f.name}: {e}")
        progress.progress((i + 1) / len(uploaded_files), text=f"Uploaded {i+1}/{len(uploaded_files)}")

    if results:
        st.success(f"Successfully uploaded {len(results)} file(s)")
        st.dataframe(pd.DataFrame(results), use_container_width=True)

st.divider()

# ---------- 2. Document Library ----------
st.header("2. Document Library")

col1, col2, col3 = st.columns(3)
with col1:
    filter_author = st.text_input("Filter by author", key="filter_author")
with col2:
    filter_type = st.selectbox("Filter by file type", ["", "pdf", "png", "jpg", "jpeg"], key="filter_type")
with col3:
    if st.button("Refresh List"):
        st.rerun()

params = {}
if filter_author:
    params["author"] = filter_author
if filter_type:
    params["file_type"] = filter_type

try:
    docs = requests.get(f"{API}/documents", params=params, timeout=10).json()
except Exception as e:
    st.error(f"Could not fetch documents: {e}")
    docs = []

if docs:
    df_docs = pd.DataFrame(docs)
    st.dataframe(df_docs, use_container_width=True)
    doc_options = [d["doc_id"] for d in docs]
else:
    st.info("No documents uploaded yet. Upload some files above to get started.")
    doc_options = []

selected_docs = st.multiselect(
    "Select specific documents to query (leave empty to search ALL documents)",
    options=doc_options
)

st.divider()

# ---------- 3. Chat / Query ----------
st.header("3. Ask the Research Agent")

if doc_options:
    if selected_docs:
        st.caption(f"Querying {len(selected_docs)} selected document(s): {', '.join(selected_docs)}")
    else:
        st.caption(f"Querying ALL {len(doc_options)} document(s)")
else:
    st.warning("Upload documents before querying.")

# Render existing chat history
for role, msg in st.session_state.chat_log:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(msg)
    else:
        with st.chat_message("assistant"):
            st.markdown(msg)

# Chat input
query = st.chat_input("Ask a question across your documents...", disabled=not doc_options)

if query:
    st.session_state.chat_log.append(("user", query))
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Agent is researching across documents..."):
            try:
                data = {"query": query, "session_id": st.session_state.session_id}
                if selected_docs:
                    data["doc_ids"] = ",".join(selected_docs)
                r = requests.post(f"{API}/query", data=data, timeout=180)
                r.raise_for_status()
                response = r.json().get("response", "No response received.")
            except requests.exceptions.Timeout:
                response = "⏱️ Request timed out. The agent may be processing too many documents — try selecting fewer documents."
            except Exception as e:
                response = f"Error: {e}"

        st.markdown(response)

    st.session_state.chat_log.append(("assistant", response))

# Clear chat button
if st.session_state.chat_log:
    if st.button("Clear Chat History"):
        st.session_state.chat_log = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()