# 📄 Agentic Document Research Chatbot

An AI-powered document research tool that lets you upload PDFs and images, then ask questions across all of them simultaneously. The agent retrieves relevant passages, cites exact sources, and synthesizes common themes across documents.

---

## 🚀 Features

- **Multi-document upload** — PDFs and images (PNG, JPG, JPEG)
- **OCR support** — Scans image-based or scanned PDFs using Tesseract
- **Semantic search** — Mistral embeddings + ChromaDB vector store
- **Agentic Q&A** — LangGraph ReAct agent with Groq (Llama 3.3 70B)
- **Structured responses** — Per-document answers with citations + synthesized themes
- **Conversation memory** — Multi-turn chat with session-based memory
- **Document filtering** — Query all documents or select specific ones
- **REST API** — FastAPI backend, Streamlit frontend

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq — `llama-3.3-70b-versatile` |
| Embeddings | Mistral — `mistral-embed` |
| Vector Store | ChromaDB |
| Agent Framework | LangGraph `create_react_agent` |
| OCR | PyMuPDF + Tesseract |
| Backend | FastAPI + SQLAlchemy (SQLite) |
| Frontend | Streamlit |

---

## 📁 Project Structure

```
├── agent.py          # LangGraph ReAct agent with memory
├── app.py            # Streamlit frontend
├── llm.py            # Groq LLM setup
├── main.py           # FastAPI backend (upload, query, list endpoints)
├── models.py         # SQLAlchemy database schema
├── processor.py      # PDF/image text extraction with OCR
├── tools.py          # LangChain tools (search, list, metadata)
├── vectorstore.py    # ChromaDB setup and retrieval
├── requirements.txt
└── .env
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/document-research-chatbot.git
cd document-research-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running Locally

Start the **FastAPI backend** (in one terminal):

```bash
uvicorn main:app --reload --port 8000
```

Start the **Streamlit frontend** (in another terminal):

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

### Frontend (Streamlit)

Deploy on [Streamlit Community Cloud]([https://streamlit.io/cloud](https://ai-document-research-chatbot-bsyheusjrhzqerx5uypjb4.streamlit.app/)):

1. Connect your GitHub repository
2. Set main file as `app.py`
3. Update the `API` variable in `app.py` to your Render backend URL:
   ```python
   API = "https://your-backend.onrender.com"
   ```

---

## 💬 How It Works

1. **Upload** — PDFs/images are processed, text is extracted (with OCR for scanned docs), chunked, embedded, and stored in ChromaDB
2. **Query** — Your question is sent to the LangGraph ReAct agent
3. **Search** — The agent calls `search_documents` tool to retrieve relevant passages from the vector store
4. **Response** — The agent returns a structured response:

```
INDIVIDUAL RESPONSES:
| Document ID | Extracted Answer         | Citation        |
|-------------|--------------------------|-----------------|
| DOC001      | Answer from document...  | Page 2, Para 3  |

SYNTHESIZED THEMES:
Theme 1 - <Title>:
Cross-document synthesis... (DOC001, DOC002)
```

---

