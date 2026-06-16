import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from agent import run_query, agent_executor
from langchain_core.messages import HumanMessage

print("=== Agent query (all docs) ===")
response = run_query("What is this document about?", session_id="test-session")
print(response)
assert "INDIVIDUAL RESPONSES" in response or "no relevant" in response.lower()

print("\n=== Agent follow-up (memory test) ===")
followup = run_query("Summarize that in one sentence.", session_id="test-session")
print(followup)

print("\n=== Inspect full message trace (tool calls) ===")
config = {"configurable": {"thread_id": "trace-session"}}
result = agent_executor.invoke(
    {"messages": [HumanMessage(content="What is this document about?")]},
    config=config
)
for msg in result["messages"]:
    msg_type = type(msg).__name__
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        print(f"{msg_type} -> TOOL CALLS: {[tc['name'] for tc in msg.tool_calls]}")
    else:
        content_preview = str(msg.content)[:150]
        print(f"{msg_type} -> {content_preview}")

print("\nPASS")