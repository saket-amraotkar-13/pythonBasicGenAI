from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

examples = [
    {
        "input": "Provide All Sales Orders created in the last 7 days",
        "output": "SELECT VBELN FROM ZSAKET_SALES WHERE ERDAT >= '2026-02-01'"
    },
    {
        "input": "Provide me total sales amount for the last 7 days",
        "output": "SELECT SUM(NETWR) FROM ZSAKET_SALES WHERE ERDAT >= '2026-02-01'"
    },
    {
        "input": "Provide gross amount for all sales orders in the last 7 days",
        "output": "SELECT VBELN, BRUTWR FROM VBAP WHERE ERDAT >= '2026-02-01'"
    },
    {
        "input": "List all customers in ZSAKET_Sales table",
        "output": "SELECT DISTINCT KUNNR FROM ZSAKET_SALES"
    }
]

system_prompt = "you are a bot helper"

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Input: {my_query}\nOutput:",
    input_variables=["my_query"]
)

llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1024, temperature=0.7)
chain = few_shot_prompt | llm | StrOutputParser()


# response = chain.invoke({"my_query": "List all customers in ZSAKET_Sales table"})
# print(response)
# OR

myprompt = few_shot_prompt.format(my_query="countries")

response = llm.invoke(myprompt)
print(response.content)


