from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate  # ← line 2: PromptTemplate → ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langserve import add_routes
from pydantic import BaseModel 
import streamlit as st
import os
from fastapi import FastAPI


load_dotenv()

os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")  # ← line 11: CLAUDE → ANTHROPIC

system_prompt = "generate a response to the user's query about SAP BTP for {language} language"

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Query: {query}")
])

llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1024, temperature=0.7)
stringparser = StrOutputParser()

chain = prompt | llm | stringparser

##choose protocol
app = FastAPI( title="SAP BTP Helper API",
                description="An API to answer questions about SAP BTP in multiple languages.",
                version="1.0"
)


###create input data model for API

class MyInput(BaseModel):
    query: str
    language: str

###using langserve to create API endpoint and consume llm 
add_routes(
    app,
    chain,
    path="/get_answer",    
    input_type=MyInput, 
    
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

### http://localhost:8000/get_answer