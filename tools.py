from langchain.tools import tool
from vectorstore import get_retriever
from models import Sessionlocal, Document

@tool
def search_documents(query: str, doc_ids: str = "") -> str:
    """Search the document knowledge base for relevant passages matching the query.
    doc_ids: optional comma-separated list of DOC IDs (e.g. 'DOC001,DOC002') to restrict search.
    Leave empty to search all documents. Returns passages with [DOC_ID | Page X, Para Y] tags."""
    ids = [d.strip() for d in doc_ids.split(",") if d.strip()] if doc_ids else None
    retriever = get_retriever(doc_ids=ids, k=10)
    results = retriever.invoke(query)
    if not results:
        return "No relevant passages found."
    formatted = []
    for r in results:
        m = r.metadata
        formatted.append(f"[{m['doc_id']} | Page {m['page']}, Para {m['paragraph']}]: {r.page_content}")
    return "\n\n".join(formatted)

@tool
def list_available_documents() -> str:
    """List all documents currently in the knowledge base with their IDs, filenames, authors, and page counts."""
    db = Sessionlocal()
    docs = db.query(Document).all()
    db.close()
    if not docs:
        return "No documents in knowledge base."
    return "\n".join(
        [f"{d.doc_id}: {d.filename} (author={d.author}, pages={d.page_count})" for d in docs]
    )

@tool
def get_document_metadata(doc_id: str) -> str:
    """Get metadata (filename, author, upload date, page count) for a specific document ID."""
    db = Sessionlocal()
    doc = db.query(Document).filter(Document.doc_id == doc_id).first()
    db.close()
    if not doc:
        return f"Document {doc_id} not found."
    return f"{doc.doc_id}: {doc.filename}, author={doc.author}, date={doc.upload_date}, pages={doc.page_count}"

ALL_TOOLS = [search_documents, list_available_documents, get_document_metadata]