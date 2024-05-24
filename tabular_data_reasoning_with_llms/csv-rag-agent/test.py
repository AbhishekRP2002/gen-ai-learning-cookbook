import pandas as pd
import logging
import sys
from IPython.display import display
from llama_index.experimental.query_engine import PandasQueryEngine
from crewai_tools import CSVSearchTool
from crewai import Agent, Task, Crew


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)


def llama_index_rag(df: pd.DataFrame, query):
    query_engine = PandasQueryEngine(df=df, verbose=True)
    response = query_engine.query(query)
    return response
    
def crewai_rag(df_path: str, query:str):
    search_tool = CSVSearchTool(df_path)
    # Define your agents with roles, goals, tools, and additional attributes
    researcher = Agent(
    role='Senior Search Expert',
    goal='Uncover hidden insights and contextual information relevant to a given query : {query} from structured data',
    backstory=(
        "You are a Senior Search Expert at a leading tech think tank."
        "Your expertise lies in identifying emerging potential context from given documents and datasets."
        "You have a knack for dissecting complex data and presenting actionable insights."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    max_rpm=100
    )
    writer = Agent(
    role='Tech Content Strategist',
    goal='Craft compelling response based given Query',
    backstory=(
        "You are a renowned Tech Content Strategist, known for your insightful and engaging articles on technology and innovation."
        "With a keen eye for detail and a flair for storytelling, you are adept at translating complex information into engaging content."
    ),
    verbose=True,
    allow_delegation=True,
    tools=[search_tool],
    cache=False, # Disable cache for this agent
    )
    # Create tasks for your agents
    task1 = Task(
    description=(
        "Understand the semantic and contextual meaning from the given CSV file"
        "Identify the key indicators that can help in framing the detailed response for the query : {query}"
    ),
    expected_output='A set of potential rows from the CSV file which are relevant to the query and are part of the solution',
    agent=researcher,
    human_input=True,
    )

    task2 = Task(
    description=(
        "Using the insights from the researcher's report,develop a compelling response to the query"
        "Your response should be well-structured and provide detailed information based on the query"
    ),
    expected_output='A comprehensive response to the query with detailed insights and relevant information',
    agent=writer
    )
    crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=2
    )
    response = crew.kickoff(inputs={'query': query})
    return response





if __name__ == '__main__':
    df = pd.read_csv('csv-rag-agent/company_test_data.csv')
    display(df.head())
    columns = df.columns
    logging.info(f'Columns: {columns}')
    query = "List the top 3 companies by employee count which uses AWS and AI ML technologies"
    response_from_llama_index = llama_index_rag(df, query)
    logging.info(f'Response from llama-index: {response_from_llama_index}')
    df_path = 'csv-rag-agent/company_test_data.csv'
    # response_from_crewai = crewai_rag(df_path, query)
    # logging.info(f'Response from crewai: {response_from_crewai}')
