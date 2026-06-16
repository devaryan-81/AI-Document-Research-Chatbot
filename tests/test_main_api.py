import requests, json

API = "http://localhost:8000"

print("=== Health check ===")
r = requests.get(f"{API}/health")
print(r.json())

print("\n=== Upload ===")
with open("tests/sample files/final_resume.pdf", "rb") as f:
    r = requests.post(f"{API}/upload", files={"file": ("sample.pdf", f)}, data={"author": "tester"})
upload_resp = r.json()
print(upload_resp)
assert upload_resp["chunks_indexed"] > 0

print("\n=== List documents ===")
r = requests.get(f"{API}/documents")
docs = r.json()
print(docs)
assert len(docs) > 0

print("\n=== Filtered list ===")
r = requests.get(f"{API}/documents", params={"author": "tester"})
print(r.json())

print("\n=== Query (agentic) ===")
r = requests.post(f"{API}/query", data={"query": "What is the main subject of this document?"})
print(json.dumps(r.json(), indent=2))
assert "response" in r.json()

print("\n=== Follow-up query (memory) ===")
r = requests.post(f"{API}/query", data={"query": "Summarize that in one sentence.", "session_id": "default"})
print(json.dumps(r.json(), indent=2))

print("\nPASS")