from langchain_anthropic import ChatAnthropic
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
os.environ["LANGSMITH_TRACING"]  = os.getenv("LANGSMITH_TRACING", "false")
os.environ["LANGSMITH_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT", "")
os.environ["LANGSMITH_API_KEY"]  = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGSMITH_PROJECT"]  = os.getenv("LANGSMITH_PROJECT", "")

user     = os.getenv('db_user')
password = os.getenv('db_password')
host     = os.getenv('db_host')
port     = os.getenv('db_port', '443')
name     = os.getenv('db_name')

connection_str = f"hana://{user}:{password}@{host}/{name}"
print(connection_str)

def connection_test():
    try:
        engine = create_engine(connection_str)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1 FROM DUMMY"))
            print(f"✅ Connection success: connected to: {name}")
        return engine
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        raise

engine = connection_test()
db = SQLDatabase(engine)

llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    temperature=0
)

# Get SQL tools from toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()
llm_with_tools = llm.bind_tools(tools)

system_prompt = """You are a helpful SQL assistant for a SAP HANA database.
Given a question, write and execute the correct SQL query and return results.
Always use double quotes around table and column names. Example: SELECT * FROM "CUSTOMER"
"""

# --- Graph nodes ---
def call_model(state: MessagesState):
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    response = llm_with_tools.invoke(messages)
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
graph.add_edge("tools", "agent")

memory = MemorySaver()
agent = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "hana_session"}}
print("Bot: Hello! Ask me anything about your HANA database.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config=config
    )
    print(f"Bot: {response['messages'][-1].content}")