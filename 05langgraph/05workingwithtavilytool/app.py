from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
import os
from tools.local_tools import my_custom_tool, update_vendor_data

load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")
os.environ["LANGSMITH_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")


tools = [TavilySearch(max_results=2), update_vendor_data,my_custom_tool]
llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1024, temperature=0.7)
llm_with_tools = llm.bind_tools(tools)

# --- Graph nodes ---
def call_model(state: MessagesState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: MessagesState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# --- Build graph ---
tool_node = ToolNode(tools)

graph = StateGraph(MessagesState)
graph.add_node("agent", call_model)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")  # after tool runs, go back to agent

memory = MemorySaver()
agent = graph.compile(checkpointer=memory)

# --- Chat loop ---
config = {"configurable": {"thread_id": "user_session"}}
print("Bot: Hello, I'm here to help.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = agent.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config
    )
    print(f"Tool Used: {response['messages'][-2].name}")
    print(f"Bot: {response['messages'][-1].content}")