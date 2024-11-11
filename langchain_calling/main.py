from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()


def explain_text(text: str) -> str:
    llm = ChatOpenAI()
    
    prompt_explain = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a assistant that explain a long text that was extracted from a invoice image document using ocr.",
        ),
        ("human", "{text}"),
    ]
    )    
    chain = prompt_explain | llm  
    msg = chain.invoke(
        {
            "text": text
        }
    )
    return msg.content
    
def query_to_llm(query: str, text: str, llm_explanation : str) -> str:
    llm = ChatOpenAI()

    prompt_query = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a assistant that explain this query {query} given that this query is about this explanation {llm_explanation} of a invoice image document, focus only in the query.",
        ),
        ("human", "{query}"),
    ]
    )    
    chain = prompt_query | llm  
    msg = chain.invoke(
        {
            "query": query,
            "llm_explanation": llm_explanation
        }
    )
    return msg.content