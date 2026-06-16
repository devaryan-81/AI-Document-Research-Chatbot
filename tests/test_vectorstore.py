import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from processor import extract_text_from_pdf
from vectorstore import add_document_chunks, get_retriever, get_collection_count

print("=== Indexing sample doc ===")
chunks = extract_text_from_pdf("tests/sample files/final_resume.pdf")
n = add_document_chunks("TEST001", chunks)
print(f"Chunks indexed: {n}")
print("Total collection count:", get_collection_count())
assert get_collection_count() > 0

print("\n=== Retriever test (single doc) ===")
retriever = get_retriever(doc_ids=["TEST001"], k=3)
results = retriever.invoke("What is this document about?")
for r in results:
    print(r.metadata, "->", r.page_content[:100])
assert len(results) > 0

print("\n=== Retriever test (all docs) ===")
retriever_all = get_retriever(k=3)
results_all = retriever_all.invoke("What is this document about?")
assert len(results_all) > 0

print("\nPASS")