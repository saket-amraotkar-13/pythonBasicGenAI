import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic

load_dotenv()
claude_api_key = os.getenv("CLAUDE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")


if claude_api_key:
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=groq_api_key)
elif groq_api_key:
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", api_key=claude_api_key)
else:
    llm = None

def generate_restaurant_recommendation(cuisine):
    # Chain 1: Get restaurant name
    prompt_1 = PromptTemplate.from_template(
        "Suggest one restaurant name that serves {cuisine} food. Reply with only the restaurant name."
    )
    chain_1 = prompt_1 | llm | StrOutputParser()

    # Chain 2: Get menu
    prompt_2 = PromptTemplate.from_template(
        "What is the menu of {restaurant_name}?"
    )
    chain_2 = prompt_2 | llm | StrOutputParser()

    # Sequential chain using LCEL
    final_chain = (
        {"restaurant_name": chain_1, "cuisine": RunnablePassthrough()}
        | RunnablePassthrough.assign(menu=chain_2)
    )

    response = final_chain.invoke({"cuisine": cuisine})
    return response

if __name__ == "__main__":
    cuisine = "Italian"
    recommendation = generate_restaurant_recommendation(cuisine)
    print(recommendation)