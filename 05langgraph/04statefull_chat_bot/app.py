from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()  # ✅ no community needed
    return store[session_id]

llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1024, temperature=0.7)

chain_with_history = RunnableWithMessageHistory(
    llm,
    get_session_history
)

session_id = "user_session"
print("Bot: Hello, I'm here to help.")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    
    response = chain_with_history.invoke(
        [HumanMessage(content=user_input)],  # ✅ pass as message list, not dict
        config={"configurable": {"session_id": session_id}}
    )
    print(f"Bot: {response.content}")