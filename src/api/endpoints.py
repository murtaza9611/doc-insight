from fastapi import APIRouter, File, UploadFile
from langchain_huggingface import HuggingFaceEmbeddings
from src.schemas.endpoints.schema import QueryRequest
from src.services.workflows.file_processing import handling_documents
from src.services.vectordb.pinecone_service import PineconeService
from src.services.llm.llm_service import LLMService
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()
embed_fn_pinecone = HuggingFaceEmbeddings(model_name='multi-qa-mpnet-base-dot-v1')
# embed_fn_pinecone = HuggingFaceEmbeddings(model_name='BAAI/bge-small-en-v1.5')

@router.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):

    try:
        logger.info("Uploadind File to vector db")

        contents = await file.read()
        file_name = file.filename
        file_extension = file_name.split(".")[-1].lower()
        logger.info("Successfully read contents of uploaded file")

        extracted_text = await handling_documents(contents, file_extension, file_name)
        logger.info("Successfully got documents list of uploaded file")

        pinecone_service = PineconeService()
        pinecone_service.create_namespace()
        logger.info("Successfully created vectordb")

        namespace_name = pinecone_service.insert_data(extracted_text)
        logger.info("Successfully inserted docs list to vector db")

        return namespace_name
    
    except Exception as ex:
        logger.critical(f"Error while uploading file: {ex}")
        raise Exception(f"Error while uploading file: {ex}")

@router.post("/query/")
async def query_vectordb(request: QueryRequest):

    try:
        logger.info("Generating response for query")
        query = request.query
        namespace_name = request.namespace_name
        llm_service = LLMService()
        pinecone_service = PineconeService()
        retriever = pinecone_service.get_retriever(namespace_name)
        chain = llm_service.get_chain(query, retriever)
        logger.info("Successfully got chain")
        
        response = chain.invoke({'query': request.query}).content
        logger.info("Successfully generated answer from chain")

        return {"query": request.query, "response": response}
    
    except Exception as ex:
        logger.critical(f"Error while answering query: {ex}")
        raise Exception(f"Error while answering query: {ex}")
