from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate  # ← line 2: PromptTemplate → ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")  # ← line 11: CLAUDE → ANTHROPIC

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are BTP Helper, a helpful assistant for SAP BTP. Answer the user's question about SAP BTP."),
    ("user", "Query: {query}")
])

llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1024, temperature=0.7)
stringparser = StrOutputParser()

chain = prompt | llm | stringparser

st.title("SAP BTP Helper")
user_query = st.text_input("Ask a question about SAP BTP:")
if st.button("Get Answer"):
    response = chain.invoke({"query": user_query})
    st.text_area("Answer:", value=response, height=300)