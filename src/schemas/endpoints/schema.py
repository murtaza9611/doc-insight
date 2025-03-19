from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    namespace_name : str