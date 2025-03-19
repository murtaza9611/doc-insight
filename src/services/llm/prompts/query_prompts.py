from langchain.prompts import PromptTemplate
from src.utils.logger import get_logger

logger = get_logger(__name__)


def get_query_prompt(query):
        
    try:
        prompt_str = """
            You are an AI assistant. Use the following retrieved context to answer the query. Answer as trtuthfully as possible from the given context.

            Input Variables:
                Context: {context}
                Query: {query}
        """
        prompt = PromptTemplate(
            input_variables=["context", "query"],
            template=prompt_str
        )
        logger.info("Successfully created prompt template out of prompt str")

        return prompt
    
    except Exception as ex:
        logger.critical(f"Error while getting query prompt: {ex}")
        raise Exception(f"Error while getting query prompt: {ex}")