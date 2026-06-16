from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.schema import Document as LCDocument

embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="documents"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

def add_document_chunks(doc_id, chunks):
    """chunks: list of {page, paragraph, sentence, text} from processor.py"""
    docs = []
    for c in chunks:
        docs.append(LCDocument(
            page_content=c["text"],
            metadata={"doc_id": doc_id, "page": c["page"], "paragraph": c["paragraph"]}
        ))
    if not docs:
        return 0
    
    split_docs = splitter.split_documents(docs)
    vectorstore.add_documents(split_docs)
    return len(split_docs)

def get_retriever(doc_ids=None, k=5):
    filter_dict = {"doc_id": {"$in": doc_ids}} if doc_ids else None
    search_kwargs = {"k": k}
    if filter_dict:
        search_kwargs["filter"] = filter_dict
    return vectorstore.as_retriever(search_kwargs=search_kwargs)

def get_collection_count():
    return vectorstore._collection.count()
    