from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from github import fetch_github_issues
# from note import note_tool


load_dotenv()

def connect_to_vstore():
    """
    Connect to the AstraDB Vector Store
    """
    embeddings = OpenAIEmbeddings()
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")

    if desired_namespace:
        ASTRA_DB_KEYSPACE = desired_namespace
    else:
        ASTRA_DB_KEYSPACE = None

    vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="github",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )
    return vstore


vstore = connect_to_vstore()
add_to_vectorstore = input("Do you want to add to the vectorstore? (y/n): ")   


vstore = connect_to_vstore()
add_to_vectorstore = input("Do you want to update the issues? (y/N): ").lower() in [
    "yes",
    "y",
]

if add_to_vectorstore:
    owner = "techwithtim"
    repo = "Flask-Web-App-Tutorial"
    issues = fetch_github_issues(owner, repo)

    try:
        vstore.delete_collection()
    except:
        pass

    vstore = connect_to_vstore()
    vstore.add_documents(issues)

    # results = vstore.similarity_search("flash messages", k=3)
    # for res in results:
    #     print(f"* {res.page_content} {res.metadata}")