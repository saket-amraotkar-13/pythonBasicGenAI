from dotenv import load_dotenv
import json
import streamlit as st
import os
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory


load_dotenv()

# Load config_sapai.json and set as environment variables
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "profiles", "config_sapai.json")
print("Config path:", config_path)
print("Config exists:", os.path.exists(config_path))

with open(config_path) as f:
    config = json.load(f)
    for key, value in config.items():
        os.environ[key] = value  # sets AICORE_AUTH_URL, AICORE_CLIENT_ID, etc.

print("AICORE_BASE_URL:", os.environ.get("AICORE_BASE_URL"))
print("AICORE_RESOURCE_GROUP:", os.environ.get("AICORE_RESOURCE_GROUP"))

dep_id = os.getenv("LLM_DEPLOYMENT_ID")
print("dep_id:", dep_id)

import requests

auth_url = os.environ.get("AICORE_AUTH_URL")
client_id = os.environ.get("AICORE_CLIENT_ID")
client_secret = os.environ.get("AICORE_CLIENT_SECRET")

resp = requests.post(
    f"{auth_url}/oauth/token",
    data={"grant_type": "client_credentials"},
    auth=(client_id, client_secret)
)
print("Auth Status:", resp.status_code)
print("Auth Response:", resp.json())

# Create proxy client — picks up env vars automatically
proxy_client = get_proxy_client("gen-ai-hub")

# Create LLM object
llm = ChatOpenAI(
    proxy_model_name="gpt-5.2",
    proxy_client=proxy_client,
    deployment_id=dep_id
)

# Initialize memory store
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


## Streamlit UI
st.title("I'm a bot")
st.write("I am here for Fun:")

## Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

## Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

## Chat input
if prompt := st.chat_input("What help do you want?"):
    ## Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    ## Get bot response
    with st.chat_message("assistant"):
        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("You are an expert assistant."),
            HumanMessagePromptTemplate.from_template("{text}")
        ])

        chain = chat_prompt | llm | StrOutputParser()

        response = chain.invoke({'text': prompt})

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
