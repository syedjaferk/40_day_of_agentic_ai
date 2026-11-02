"""An agent that searches only when it needs to."""

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from model import llm
from retriever_tool import search_handbook

SYSTEM = (
    "You are the Parottasalna Academy assistant.\n"
    "For questions about the academy, call search_handbook and answer ONLY from what it returns, "
    "naming the source in brackets.\n"
    "If the handbook does not contain the answer, say you don't know. Do not guess.\n"
    "For greetings or small talk, answer directly without searching."
)

agent = create_agent(
    model=llm,
    tools=[search_handbook],
    system_prompt=SYSTEM,
    checkpointer=InMemorySaver(),
)


def ask(question, thread="demo"):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        {"configurable": {"thread_id": thread}},
    )
    print("# " * 30)
    for m in result["messages"]:
        if m.type == "ai" and m.tool_calls:
            print("   🔎 searched:", [c["args"]["query"] for c in m.tool_calls])
    print("🤖", result["messages"][-1].content)


if __name__ == "__main__":
    ask("Hi!")
    ask("How many days do I have to cancel and get my money back?")
    ask(
        "And how do I request it?"
    )  # follow-up: the agent rewrites the query using the history
    ask("Who is the CEO of the academy?")  # not in the handbook
