import os
import random, string, datetime
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from src.utils.logger import get_logger
from src.core.config import settings

logger = get_logger(__name__)
load_dotenv()

# Use when using .env file
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

#Use when using streamlit secret file
PINECONE_API_KEY = settings.PINECONE_API_KEY

# embed_fn_pinecone = HuggingFaceEmbeddings(model_name='BAAI/bge-small-en-v1.5')
embed_fn_pinecone = HuggingFaceEmbeddings(model_name='multi-qa-mpnet-base-dot-v1')

class PineconeService:
    def __init__(self):
        self.pc = Pinecone(pinecone_api_key=PINECONE_API_KEY)
        self.index_name = "doc-insight-01"
        self.namespace_name = ''.join(random.sample(string.ascii_uppercase, 4) + random.sample(string.ascii_lowercase, 4) + random.sample(string.digits, 4)) + '_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def create_namespace(self):
        """Creates a new Pinecone index."""
        try:
            logger.info("Checking if index exists")
            if self.index_name not in self.pc.list_indexes().names():
                logger.info("Index does not exist. Creating index")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=768,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )

            index = self.pc.Index(self.index_name)
            index_stats = index.describe_index_stats()

            logger.info("Checking if namespace exists")
            if self.namespace_name in index_stats["namespaces"]:
                logger.info("Namespace found. Deleting previous namespace")
                index.delete(delete_all=True, namespace=self.namespace_name)

            logger.info("Creaating namespace")
            return PineconeVectorStore(index=index, embedding=embed_fn_pinecone, namespace=self.namespace_name)
        
        except Exception as ex:
            logger.critical(f"Error while creating namespace of pinecone vectordb: {ex}")
            raise Exception(f"Error while creating namespace of pinecone vectordb: {ex}")

    def insert_data(self, documents):
        """Inserts documents into Pinecone."""
        try:
            logger.info("Inserting docs into vectordb")
            PineconeVectorStore.from_documents(
                documents, embed_fn_pinecone, index_name=self.index_name, namespace=self.namespace_name
            )
            return self.namespace_name
        
        except Exception as ex:
            logger.critical(f"Error while inserting data into pinecone vectordb: {ex}")
            raise Exception(f"Error while inserting data into pinecone vectordb: {ex}")

    def load_index(self, namespace_name):
        """Loads an existing Pinecone vector database."""
        try:
            INDEX_NAME = self.index_name
            

            logger.info("Loading an existing vector db")
            pinecone_store = PineconeVectorStore.from_existing_index(index_name = INDEX_NAME, embedding = embed_fn_pinecone, namespace = namespace_name)

            return pinecone_store
        except Exception as e:
            logger.critical(f"Error while loading vectordb:'{str(e)}'")
            raise Exception(f"Error while loading vectordb:'{str(e)}'")
        
    def get_retriever(self,namespace_name):
            
        try:
            vectordb = self.load_index(namespace_name)
            logger.info("Existing vectordb loaded")

            logger.info("Loading vector db retriever")
            retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})

            return retriever
        
        except Exception as ex:
            logger.critical(f"Error while loading vector db retriever: {ex}")
            raise Exception(f"Error while loading vector db retriever: {ex}")
