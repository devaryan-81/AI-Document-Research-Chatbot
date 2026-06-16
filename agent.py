from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage

from llm import llm
from tools import ALL_TOOLS

SYSTEM_PROMPT = """You are a research assistant analyzing a corpus of documents.

For every user query:
1. Use search_documents to retrieve relevant passages (across all or selected documents).
   Call it multiple times with varied phrasing if needed for thorough coverage.
2. For EACH document that has relevant content, extract a concise 1-2 sentence answer
   with its exact citation (Page, Paragraph) as returned by the tool.
3. After gathering per-document answers, identify 2-5 coherent common THEMES across documents.
4. Output your final answer in exactly this format:

INDIVIDUAL RESPONSES:
| Document ID | Extracted Answer | Citation |
|---|---|---|
| DOC001 | <answer> | Page X, Para Y |

SYNTHESIZED THEMES:
Theme 1 - <Title>:
<2-3 sentence synthesis> (DOC_IDs)

Theme 2 - <Title>:
<2-3 sentence synthesis> (DOC_IDs)

Rules:
- Never fabricate citations not returned by search_documents.
- If no relevant passages are found for a document, omit it from the table.
- If nothing relevant is found at all, say so clearly without inventing themes.
"""

checkpointer = InMemorySaver()

agent_executor = create_react_agent(
    model=llm,
    tools=ALL_TOOLS,
    prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

def run_query(query: str, doc_ids: list[str] = None, session_id: str = "default") -> str:
    full_input = query
    if doc_ids:
        full_input += f"\n\n(Restrict search to these document IDs: {','.join(doc_ids)})"

    config = {"configurable": {"thread_id": session_id}}
    result = agent_executor.invoke(
        {"messages": [HumanMessage(content=full_input)]},
        config=config
    )
    # Last message in the state is the agent's final response
    return result["messages"][-1].content