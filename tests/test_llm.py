import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from llm import llm

print("==== Basic LLM Call ====")
resp = llm.invoke("Say 'OK' if you can read this.")
print(resp.content)
assert "OK" in resp.content.upper()

print("\nPASS")
