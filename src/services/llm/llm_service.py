import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableMap
from operator import itemgetter
from src.services.llm.prompts.query_prompts import get_query_prompt
from src.services.vectordb.pinecone_service import PineconeService
from src.utils.combine_documents import combine_documents
from src.core.config import settings


load_dotenv()

# Use when using .env file
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#Use when using streamlit secret file
OPENAI_API_KEY = settings.OPENAI_API_KEY

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
    
    def get_chain(self, query,retriever):
        prompt = get_query_prompt(query)
        llm = self.llm

        retrieval_chain = RunnableMap({
            "context": itemgetter("query") | retriever | combine_documents,
            "query": itemgetter("query"),
        }) | prompt | llm

        return retrieval_chain
