from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import Docx2txtLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)

class IncomingFileProcessor():
    def __init__(self, chunk_size=750) -> None:
        self.chunk_size = chunk_size
    
    def get_pdf_splits(self, pdf_file: str, filename: str):
        try:
            loader = PyMuPDFLoader(pdf_file)
            pages = loader.load()
            logger.info("Succesfully loaded the pdf file")

            textsplit = RecursiveCharacterTextSplitter(
                separators=["\n\n",".","\n"],
                chunk_size=self.chunk_size, chunk_overlap=15, 
                length_function=len)
            
            doc_list = []
            for pg in pages:
                pg_splits = textsplit.split_text(pg.page_content)
                for page_sub_split in pg_splits:
                    metadata = {"source": filename}
                    doc_string = Document(page_content=page_sub_split, metadata=metadata)
                    doc_list.append(doc_string)
            logger.info("Succesfully split the pdf file")

            return doc_list
        
        except Exception as e:
            logger.critical(f"Error in loading/splitting pdf file: {str(e)}")
            raise Exception(str(e))
        
    def get_docx_splits(self, docx_file: str, filename: str):
        try:
            loader = Docx2txtLoader(str(docx_file))
            txt = loader.load()
            logger.info("Succesfully loaded the docx file")

            textsplit = RecursiveCharacterTextSplitter(
                separators=["\n\n",".","\n"],
                chunk_size=self.chunk_size, chunk_overlap=15, 
                length_function=len)
            doc_list = textsplit.split_text(txt[0].page_content)

            new_doc_list = []
            for page_sub_split in doc_list:
                metadata = {"source": filename}
                doc_string = Document(page_content=page_sub_split, metadata=metadata)
                new_doc_list.append(doc_string)
            logger.info("Succesfully split the docx file")

            return new_doc_list
        
        except Exception as e:
            logger.critical("Error in Loading docx file:"+str(e))
            raise Exception(str(e))
