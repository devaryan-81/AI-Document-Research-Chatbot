from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil, os

from processor import extract_text_from_pdf, extract_text_from_image
from vectorstore import add_document_chunks, get_collection_count
from models import Sessionlocal, Document
from agent import run_query

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...), author: str = Form(None)):
    db = Sessionlocal()
    count = db.query(Document).count()
    doc_id = f"DOC{count+1:03d}"

    filepath = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    ext = file.filename.split(".")[-1].lower()
    if ext == "pdf":
        chunks = extract_text_from_pdf(filepath)
        pages = max((c["page"] for c in chunks), default=0)
    else:
        chunks = extract_text_from_image(filepath)
        pages = 1

    indexed = add_document_chunks(doc_id, chunks)

    doc = Document(doc_id=doc_id, filename=file.filename, file_type=ext,
                    author=author, page_count=pages)
    db.add(doc)
    db.commit()
    db.close()

    return {"doc_id": doc_id, "filename": file.filename, "chunks_indexed": indexed}

@app.get("/documents")
def list_documents(author: str = None, file_type: str = None):
    db = Sessionlocal()
    query = db.query(Document)
    if author:
        query = query.filter(Document.author == author)
    if file_type:
        query = query.filter(Document.file_type == file_type)
    docs = query.all()
    result = [{"doc_id": d.doc_id, "filename": d.filename, "author": d.author,
               "file_type": d.file_type, "upload_date": d.upload_date,
               "pages": d.page_count} for d in docs]
    db.close()
    return result

@app.post("/query")
def query_endpoint(query: str = Form(...), doc_ids: str = Form(None), session_id: str = Form("default")):
    ids = [d.strip() for d in doc_ids.split(",") if d.strip()] if doc_ids else None
    response = run_query(query, doc_ids=ids, session_id=session_id)
    return {"response": response}

@app.get("/health")
def health():
    return {"status": "ok", "indexed_chunks": get_collection_count()}