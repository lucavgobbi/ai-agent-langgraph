import os
from langchain.chat_models import init_chat_model

def get_llm(tools):
    llm = init_chat_model(
        "azure_openai:gpt-4.1-nano",
        azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    )
    
    llm_with_tools = llm.bind_tools(tools)
    return llm_with_tools