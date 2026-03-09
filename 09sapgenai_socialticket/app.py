## 1. Dependencies
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from hana_ml import dataframe
from hdbcli import dbapi
from datetime import datetime
import os
import logging
import pandas as pd
import hana_ml
import json

## 2. Load environment variables
load_dotenv()

## 3. Prepare Logging
FORMAT = "%(asctime)s:%(name)s:%(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

## 4. Load SAP AI Core config from local JSON
config_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "profiles", "config_sapai.json"
)

if os.path.exists(config_path):
    with open(config_path) as f:
        config = json.load(f)
        for key, value in config.items():
            os.environ[key] = value
    logging.info("Loaded SAP AI Core config from config_sapai.json")
else:
    logging.warning(f"Config file not found at: {config_path}")

## 5. HANA connection config
hana = {
    'credentials': {
        'host':     os.getenv("HANA_HOST"),
        'port':     os.getenv("HANA_PORT", "443"),
        'user':     os.getenv("HANA_USER"),
        'password': os.getenv("HANA_PASSWORD"),
    }
}

## Validate required HANA env variables
required_vars = ['HANA_HOST', 'HANA_USER', 'HANA_PASSWORD']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    logging.error(f"Missing required env variables: {missing_vars}")
    hana = None
else:
    logging.info(f"HANA connection configured for host: {hana['credentials']['host']}")


## 6. Define class
class issue_reporting_app():

    def __init__(self, input_message) -> None:
        self.input_message = input_message

        self.info_dict = {
            "category":
            '''Classify the post in one of the following Categories: "PUBLIC CLEANLINESS", "ROAD & FOOTPATHS", \
            "FACILITY & PARK MAINTENANCE", "PESTS", "DRAIN". \
            If none of the categories fit, return "OTHER".''',

            "Priority":
            '''Identify the Priority to be given to the reported issue: "4-Low", "3-Medium", "2-High", "1-Very High".
                4-Low: Issue is not critical, can be managed over time.
                3-Medium: Issue has some significant negative impact on peoples life.
                2-High: Issue is critical and needs to be addressed ASAP.
                1-Very High: Issue is very critical, danger to peoples life.''',

            "summary":
            "Summarize the reported issue in 40 characters and a neutral tone",

            "description":
            "Summarize the reported issue within 400 characters and a neutral tone",

            "address":
            "Extract the address where the issue is reported",

            "sentiments":
            '''Classify the sentiments of the post into "NEUTRAL", "NEGATIVE", "VERY NEGATIVE".
            1. NEUTRAL: issue is reported in a polite tone
            2. NEGATIVE: post indicates irony, impatience, annoyance
            3. VERY NEGATIVE: post is rude and abusive'''
        }

        self.template_string = '''Extract the information from the social media post delimited by triple backticks.
            ```{POST}```'''

        self.functions = [
            {
                "name": "post_analysis",
                "description": "Analyze social media post and extract structured information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Classified category of the issue"
                        },
                        "priority": {
                            "type": "string",
                            "description": "Priority level of the issue"
                        },
                        "summary": {
                            "type": "string",
                            "description": "40 character summary"
                        },
                        "description": {
                            "type": "string",
                            "description": "400 character detailed description"
                        },
                        "address": {
                            "type": "string",
                            "description": "Location address of the issue e.g. lat,long"
                        },
                        "sentiments": {
                            "type": "string",
                            "description": "Sentiment classification of the post"
                        }
                    },
                    "required": ["category", "priority", "summary", "description", "address", "sentiments"]
                }
            }
        ]

        self.extracted_data = None
        self.output = None
        self.guid = None
        self.conn_context = None

    ## Get UUID from SAP HANA
    def get_uuid(self) -> str:
        if hana is not None:
            try:
                conn = dbapi.connect(
                    address=hana['credentials']['host'],
                    port=int(hana['credentials']['port']),
                    user=hana['credentials']['user'],
                    password=hana['credentials']['password']
                )
                cursor = conn.cursor()
                cursor.execute("SELECT TO_NVARCHAR(SYSUUID) FROM DUMMY")
                guid = cursor.fetchone()[0]
                logging.info(f"Generated GUID: {guid}")
                cursor.close()
                conn.close()
                return str(guid)
            except Exception as e:
                logging.error(f"Error generating GUID: {e}")
                return None
        else:
            logging.error("HANA connection not available for GUID generation")
            return None

    ## Set DB connection and generate GUID
    def set_db_connection(self) -> None:
        if hana is not None:
            try:
                self.conn_context = hana_ml.dataframe.ConnectionContext(
                    address=hana['credentials']['host'],
                    port=int(hana['credentials']['port']),
                    user=hana['credentials']['user'],
                    password=hana['credentials']['password']
                )
                self.guid = self.get_uuid()
                logging.info(f"DB connection established. GUID: {self.guid}")
            except Exception as e:
                logging.error(f"Error setting DB connection: {e}")
                self.conn_context = None
                self.guid = None
        else:
            self.conn_context = None
            self.guid = None
            logging.error("HANA configuration not available")

    ## Check connection to SAP HANA BTP HDI
    def check_conn(self) -> None:
        if hana is not None:
            try:
                conn = dbapi.connect(
                    address=hana['credentials']['host'],
                    port=int(hana['credentials']['port']),
                    user=hana['credentials']['user'],
                    password=hana['credentials']['password']
                )
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM DUMMY")
                result = cursor.fetchone()
                if result:
                    logging.info("HANA connection established successfully")
                else:
                    logging.warning("HANA connection test returned no result")
                cursor.close()
                conn.close()
            except Exception as e:
                logging.error(f"Failed to establish HANA connection: {e}")
        else:
            logging.error("HANA configuration not available")

    ## Prepare the content string to send to LLM
    def prepare_content(self) -> None:
        self.message = (
            "redditPostId: " + self.input_message["id"] +
            ", author: " + self.input_message["author"] +
            ", title: " + self.input_message["title"] +
            ", message: " + self.input_message["longText"] +
            ", postingDate: " + self.input_message["postingdate"]
        )
        logging.info(f"Prepared content: {self.message}")

    ## Call LLM via SAP Gen AI Hub and extract structured JSON
    def ask_llm(self) -> None:
        try:
            dep_id = os.getenv("LLM_DEPLOYMENT_ID")
            proxy_client = get_proxy_client("gen-ai-hub")

            llm = ChatOpenAI(
                proxy_client=proxy_client,
                deployment_id=dep_id
            )

            system_message = SystemMessagePromptTemplate.from_template(
                "You are an AI assistant that analyzes social media posts about public issues. "
                "Extract the following information: {info_dict}"
            )
            human_message = HumanMessagePromptTemplate.from_template(self.template_string)
            chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])

            # Bind functions for structured output
            model = llm.bind(functions=self.functions)

            # Build chain
            chain = chat_prompt | model | JsonOutputFunctionsParser()

            result = chain.invoke({
                "POST": self.message,
                "info_dict": str(self.info_dict)
            })

            self.extracted_data = result
            logging.info(f"Extracted data: {self.extracted_data}")

        except Exception as e:
            logging.error(f"Error in ask_llm: {e}")
            self.extracted_data = None

    ## Prepare DataFrame from LLM result for DB insert
    def prepare_output(self) -> None:
        if self.extracted_data is None:
            logging.error("No extracted data to prepare output from")
            self.output = None
            return

        output = pd.DataFrame([self.extracted_data])

        output = output.rename(columns={
            'sentiments':  'SENTIMENT',
            'address':     'LOCATION',
            'summary':     'GENAISUMMARY',
            'description': 'GENAIDESCRIPTION',
            'priority':    'PRIORITY',
            'category':    'CATEGORY'
        })

        # Split lat/long from address field
        if 'LOCATION' in output.columns:
            try:
                output[['LAT', 'LONG']] = (
                    output['LOCATION']
                    .str.split(',', n=1, expand=True)
                    .astype(float)
                )
            except Exception as e:
                logging.warning(f"Could not parse LAT/LONG from address: {e}")
                output['LAT'] = None
                output['LONG'] = None

        # Drop LOCATION column - not in CUST_TICKETS table (only LAT/LONG are)
        output = output.drop(columns=['LOCATION'], errors='ignore')

        # Add metadata columns
        output['ID']           = self.guid
        output['REDDITPOSTID'] = self.input_message.get("id")
        output['REPORTEDBY']   = self.input_message.get("author")
        output['DATE']         = datetime.now().date()
        output['TIME']         = datetime.now().time()
        output['PRIORITYDESC'] = output.get('PRIORITY', '')

        self.output = output
        logging.info(f"Output DataFrame prepared with {len(output)} rows")
        logging.info(f"Output columns: {list(output.columns)}")
        logging.info(f"Output data:\n{output.to_string()}")

    ## Insert DataFrame to SAP HANA table in HDI
    def write_table_to_hana(self, df, table_name, schema) -> None:
        if self.conn_context is None:
            logging.error("No DB connection context available for write")
            return
        try:
            dataframe.create_dataframe_from_pandas(
                connection_context=self.conn_context,
                schema=schema,
                pandas_df=df,
                table_name=table_name,
                force=False,
                replace=False,
                append=True
            )
            logging.info(f"Data written to {schema}.{table_name} successfully")
        except Exception as e:
            logging.error(f"Error writing to HANA table: {e}")

    ## Orchestration workflow — returns dict for Flask response
    def run_workflow(self) -> dict:
        self.set_db_connection()
        self.prepare_content()
        self.ask_llm()
        self.prepare_output()
        if self.output is not None:
            self.write_table_to_hana(
                self.output,
                "CUST_TICKETS",
                "USR_5LRWIWBIQOD8QJDMH5WRSQU8P"
            )
            return {"status": "success", "id": self.guid, "data": self.extracted_data}
        else:
            logging.error("Workflow aborted: output DataFrame is None")
            return {"status": "error", "message": "Output DataFrame is None"}


if __name__ == "__main__":
    input_message = {
        "id": "rdt-232123221",
        "author": "Srikant Dheekonda",
        "title": "I am not able to walk also",
        "longText": """Before Jan 2026, getting to office was quick in peak hours for 6-10 KMs, \
but now it's taking hours, latitude: 30.4421, Longitude: -97.6339.""",
        "postingdate": "2026-01-12"
    }

    app = issue_reporting_app(input_message)
    app.run_workflow()
