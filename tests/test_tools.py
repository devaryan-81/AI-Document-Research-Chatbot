import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from tools import search_documents, list_available_documents, get_document_metadata

print("=== list_available_documents ===")
print(list_available_documents.invoke({}))

print("\n=== search_documents (all docs) ===")
result = search_documents.invoke({"query": "main subject", "doc_ids": ""})
print(result[:500])
assert result, "Empty search result"

print("\n=== search_documents (restricted to TEST001) ===")
result_restricted = search_documents.invoke({"query": "main subject", "doc_ids": "TEST001"})
print(result_restricted[:500])

print("\n=== get_document_metadata ===")
print(get_document_metadata.invoke({"doc_id": "TEST001"}))
print(get_document_metadata.invoke({"doc_id": "NOTREAL"}))

print("\nPASS")